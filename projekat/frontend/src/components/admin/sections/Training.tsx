import KnowledgePendingList from "../KnowledgePendingList";

export default function Training() {
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Training Dataset</h2>
      </div>
      <KnowledgePendingList />
    </div>
  );
}
