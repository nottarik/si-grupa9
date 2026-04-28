export default function Dashboard() {
  const stats = [
    { label: "Avg. Rating", val: "4.3", sub: "Last 30 days", icon: "★" },
    { label: "Total Calls", val: "1,284", sub: "This month", icon: "📞" },
    { label: "Transcripts", val: "342", sub: "Processed", icon: "📄" },
    { label: "Open Issues", val: "6", sub: "Requires attention", icon: "⚠" },
  ];

  const ratingPcts: Record<number, number> = { 5: 48, 4: 30, 3: 12, 2: 6, 1: 4 };

  const activity = [
    { txt: "New transcript uploaded", time: "2 min ago" },
    { txt: "Issue #4 opened by Tomislav R.", time: "1h ago" },
    { txt: "3 training items approved", time: "3h ago" },
    { txt: "Audio transcription completed", time: "5h ago" },
    { txt: "Chat log report exported", time: "Yesterday" },
  ];

  return (
    <div className="space-y-6">
      <h2 className="section-title">Dashboard</h2>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="stat-card">
            <div className="text-2xl mb-1">{s.icon}</div>
            <div className="text-2xl font-bold text-charcoal font-cinzel">{s.val}</div>
            <div className="text-xs font-semibold text-gold mt-1">{s.label}</div>
            <div className="text-xs text-gray-400 mt-0.5">{s.sub}</div>
          </div>
        ))}
      </div>

      <div className="meander" />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Rating distribution */}
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
            Rating Distribution
          </div>
          {[5, 4, 3, 2, 1].map((n) => (
            <div key={n} className="flex items-center gap-3 mb-2">
              <span className="text-xs w-4 text-gray-500">{n}★</span>
              <div className="flex-1 bg-gray-100 rounded-full h-2">
                <div
                  className="h-2 rounded-full"
                  style={{
                    width: `${ratingPcts[n]}%`,
                    background: "linear-gradient(90deg,#e0c070,#C5A059)",
                  }}
                />
              </div>
              <span className="text-xs text-gray-400 w-8">{ratingPcts[n]}%</span>
            </div>
          ))}
        </div>

        {/* Recent activity */}
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
            Recent Activity
          </div>
          {activity.map((a, i) => (
            <div
              key={i}
              className="flex justify-between items-center py-2 border-b last:border-0"
              style={{ borderColor: "rgba(197,160,89,0.1)" }}
            >
              <span className="text-sm text-charcoal">{a.txt}</span>
              <span className="text-xs text-gray-400">{a.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
