import { useState } from "react";
import KnowledgePendingList from "../KnowledgePendingList";
import KnowledgeApprovedList from "../KnowledgeApprovedList";
import KnowledgeManualEntry from "../KnowledgeManualEntry";

type Tab = "baza" | "cekanje";

export default function Training() {
  const [tab, setTab] = useState<Tab>("baza");

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Knowledge Base</h2>
      </div>

      <KnowledgeManualEntry />

      <div className="flex gap-1 border-b border-gold/20">
        {(["baza", "cekanje"] as Tab[]).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-xs font-semibold tracking-wide transition-colors ${
              tab === t
                ? "border-b-2 border-gold text-gold"
                : "text-gray-400 hover:text-charcoal"
            }`}
            style={tab === t ? { borderColor: "rgba(197,160,89,0.9)", color: "rgba(197,160,89,0.95)" } : {}}
          >
            {t === "baza" ? "Knowledge Base" : "Pending Review"}
          </button>
        ))}
      </div>

      {tab === "baza" && <KnowledgeApprovedList />}
      {tab === "cekanje" && <KnowledgePendingList />}
    </div>
  );
}
