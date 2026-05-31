import KnowledgeApprovedList from "../KnowledgeApprovedList";
import KnowledgeManualEntry from "../KnowledgeManualEntry";

export default function Training() {
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Knowledge Base</h2>
      </div>

      <KnowledgeManualEntry />

      <KnowledgeApprovedList />
    </div>
  );
}
