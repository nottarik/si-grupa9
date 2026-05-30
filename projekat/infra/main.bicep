// ---------------------------------------------------------------------------
// Single-click deploy infra for the RAG chatbot (compute only).
//
// Provisions:
//   - Log Analytics + Container Apps managed environment
//   - Azure Container Registry + user-assigned identity (AcrPull) so azd can
//     push/pull the backend image
//   - Container App `backend` (FastAPI), 1 vCPU / 2 GiB, always-warm (min 1)
//   - Static Web App `web` (Free) for the Vite frontend
//
// Data services (Supabase / Qdrant Cloud / Groq) stay external — only their
// connection secrets are injected here.
//
// Deployed by `azd up`. Resource-group scoped: azd creates the resource group.
// ---------------------------------------------------------------------------
targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the azd environment — used to tag resources.')
param environmentName string

@minLength(1)
@description('Primary location for the backend / registry / environment.')
param location string

@description('Region for the Static Web App (Free SKU is region-limited).')
@allowed([
  'westus2'
  'centralus'
  'eastus2'
  'westeurope'
  'eastasia'
])
param staticWebAppLocation string = 'westeurope'

@description('Backend container image. azd sets this to the built image after the first build.')
param backendImageName string = ''

// --- Secrets (supplied via azd env -> main.parameters.json; never committed) ---
@secure()
param databaseUrl string
@secure()
param qdrantUrl string
@secure()
param qdrantApiKey string
@secure()
param groqApiKey string
@secure()
param supabaseUrl string
@secure()
param supabaseServiceKey string
@secure()
@description('Fernet key for PII token maps. MUST reuse the existing value — a new key makes already-masked data undecryptable.')
param tokenMapKey string
@secure()
@description('Base64-encoded service-account JSON. Base64 is used because the raw JSON contains quotes/newlines that corrupt the azd parameters file during substitution; it is decoded back to JSON below.')
param googleServiceAccountJsonBase64 string = ''
param googleDriveTranscriptsFolderId string = ''

// Generated per deploy — SECRET_KEY rotation only forces users to log in again.
@secure()
param secretKey string = newGuid()
@secure()
param internalApiKey string = newGuid()

var resourceToken = toLower(uniqueString(resourceGroup().id, environmentName))
var tags = { 'azd-env-name': environmentName }
var acrPullRoleId = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')

// --- Observability ---
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

// --- Container registry + identity (so azd can push and the app can pull) ---
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'acr${resourceToken}'
  location: location
  tags: tags
  sku: { name: 'Basic' }
  properties: { adminUserEnabled: false }
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${resourceToken}'
  location: location
  tags: tags
}

resource acrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: containerRegistry
  name: guid(containerRegistry.id, identity.id, acrPullRoleId)
  properties: {
    roleDefinitionId: acrPullRoleId
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// --- Container Apps environment ---
resource containerAppsEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'cae-${resourceToken}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// --- Static Web App (frontend) ---
resource web 'Microsoft.Web/staticSites@2023-12-01' = {
  name: 'swa-${resourceToken}'
  location: staticWebAppLocation
  tags: union(tags, { 'azd-service-name': 'web' })
  sku: { name: 'Free', tier: 'Free' }
  properties: {
    allowConfigFileUpdates: true
  }
}

// --- Backend Container App ---
resource backend 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-backend-${resourceToken}'
  location: location
  tags: union(tags, { 'azd-service-name': 'backend' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    managedEnvironmentId: containerAppsEnv.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto' // enables the WSS upgrade used by the chat/escalation sockets
        allowInsecure: false
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: identity.id
        }
      ]
      secrets: [
        { name: 'database-url', value: databaseUrl }
        { name: 'qdrant-url', value: qdrantUrl }
        { name: 'qdrant-api-key', value: qdrantApiKey }
        { name: 'groq-api-key', value: groqApiKey }
        { name: 'supabase-url', value: supabaseUrl }
        { name: 'supabase-service-key', value: supabaseServiceKey }
        { name: 'token-map-key', value: tokenMapKey }
        { name: 'google-service-account-json', value: empty(googleServiceAccountJsonBase64) ? '' : base64ToString(googleServiceAccountJsonBase64) }
        { name: 'secret-key', value: secretKey }
        { name: 'internal-api-key', value: internalApiKey }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: !empty(backendImageName) ? backendImageName : 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            { name: 'PORT', value: '8000' }
            { name: 'APP_ENV', value: 'production' }
            { name: 'ACCESS_TOKEN_EXPIRE_MINUTES', value: '60' }
            { name: 'QDRANT_COLLECTION_NAME', value: 'knowledge_base' }
            { name: 'EMBEDDING_MODEL', value: 'all-MiniLM-L6-v2' }
            { name: 'LLM_MODEL', value: 'llama-3.3-70b-versatile' }
            { name: 'WHISPER_MODEL', value: 'whisper-large-v3' }
            { name: 'RAG_TOP_K', value: '5' }
            { name: 'RAG_CONFIDENCE_THRESHOLD', value: '0.5' }
            { name: 'SUPABASE_BUCKET', value: 'supabucket' }
            { name: 'GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID', value: googleDriveTranscriptsFolderId }
            { name: 'ALLOWED_ORIGINS', value: 'https://${web.properties.defaultHostname}' }
            { name: 'DATABASE_URL', secretRef: 'database-url' }
            { name: 'QDRANT_URL', secretRef: 'qdrant-url' }
            { name: 'QDRANT_API_KEY', secretRef: 'qdrant-api-key' }
            { name: 'GROQ_API_KEY', secretRef: 'groq-api-key' }
            { name: 'SUPABASE_URL', secretRef: 'supabase-url' }
            { name: 'SUPABASE_SERVICE_KEY', secretRef: 'supabase-service-key' }
            { name: 'TOKEN_MAP_KEY', secretRef: 'token-map-key' }
            { name: 'GOOGLE_SERVICE_ACCOUNT_JSON', secretRef: 'google-service-account-json' }
            { name: 'SECRET_KEY', secretRef: 'secret-key' }
            { name: 'INTERNAL_API_KEY', secretRef: 'internal-api-key' }
          ]
          // No explicit probes: the first provision runs a placeholder image (port 80,
          // no /health) before the real image is deployed, so a /health:8000 probe would
          // fail-loop against it. Container Apps' default health handling plus the
          // always-warm replica below cover the real container's ~30–60s model load.
        }
      ]
      scale: {
        minReplicas: 1 // always warm — no per-request model-load cold start
        maxReplicas: 1
      }
    }
  }
}

// Consumed by azd: where to push the built image.
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.properties.loginServer
// Baked into the frontend build so the SPA calls the right backend.
output VITE_API_URL string = 'https://${backend.properties.configuration.ingress.fqdn}'
// Convenience.
output BACKEND_URI string = 'https://${backend.properties.configuration.ingress.fqdn}'
output WEB_URI string = 'https://${web.properties.defaultHostname}'
