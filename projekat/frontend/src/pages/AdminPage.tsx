import TranscriptUpload from "../components/admin/TranscriptUpload";
import KnowledgePendingList from "../components/admin/KnowledgePendingList";

export default function AdminPage() {
  return (
    <div className="max-w-4xl mx-auto w-full px-4 py-8 flex flex-col gap-8">
      <h1 className="text-2xl font-bold text-gray-800">Admin panel</h1>

      {/* Upload section */}
      <section>
        <TranscriptUpload />
      </section>

      {/* Pending Q&A approval section */}
      <section>
        <h2 className="font-semibold text-gray-700 mb-4">
          Q&amp;A parovi koji čekaju odobrenje
        </h2>
        <KnowledgePendingList />
      </section>
    </div>
  );
}
