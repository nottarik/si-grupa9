import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './LandingPage.css';

export default function LandingPage() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return null;
  if (isAuthenticated) return <Navigate to="/chat" replace />;

  return (
    <div className="lp">

      {/* ── NAV ── */}
      <nav>
        <div className="nav-inner">
          <a href="#top" className="nav-logo">
            <svg width="22" height="14" viewBox="0 0 90 50" fill="none" style={{color: 'var(--gold)'}}>
              <path d="M44 42 Q38 36 30 30 Q20 22 12 18" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.5"/>
              <path d="M12 18 Q8 12 14 8 Q20 6 21 14 Q17 15 12 18" fill="currentColor" opacity="0.7"/>
              <path d="M22 14 Q20 7 27 5 Q34 3 34 12 Q29 13 22 14" fill="currentColor" opacity="0.75"/>
              <path d="M34 11 Q34 4 41 3 Q48 2 47 11 Q42 12 34 11" fill="currentColor" opacity="0.85"/>
              <path d="M10 18 Q4 16 3 22 Q2 28 9 27 Q10 22 10 18" fill="currentColor" opacity="0.5"/>
            </svg>
            AMBASSADOR
          </a>
          <div className="nav-links">
            <a href="#how">How it works</a>
            <a href="#features">Features</a>
            <a href="#usecases">Use cases</a>
            <Link to="/login" className="nav-cta">Sign In</Link>
          </div>
        </div>
      </nav>

      {/* ── HERO ── */}
      <header className="hero marble" id="top">
        <div className="hero-inner">
          <div className="hero-laurel">
            <svg width="120" height="40" viewBox="0 0 200 70" fill="none">
              <g transform="translate(0,0)">
                <path d="M88 50 Q80 44 70 38 Q56 28 42 22" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.5"/>
                <path d="M40 22 Q34 14 42 10 Q50 8 51 18 Q46 19 40 22" fill="currentColor" opacity="0.75"/>
                <path d="M52 18 Q48 9 58 6 Q68 3 67 14 Q60 16 52 18" fill="currentColor" opacity="0.8"/>
                <path d="M68 14 Q66 5 76 3 Q86 2 84 14 Q76 15 68 14" fill="currentColor" opacity="0.85"/>
                <path d="M40 22 Q32 20 30 26 Q28 34 38 32 Q40 27 40 22" fill="currentColor" opacity="0.55"/>
                <path d="M50 30 Q42 30 41 38 Q40 46 50 44 Q51 37 50 30" fill="currentColor" opacity="0.6"/>
                <path d="M64 38 Q56 38 55 46 Q54 54 64 52 Q65 45 64 38" fill="currentColor" opacity="0.7"/>
              </g>
              <circle cx="100" cy="35" r="2.5" fill="currentColor" opacity="0.7"/>
              <g transform="translate(200,0) scale(-1,1)">
                <path d="M88 50 Q80 44 70 38 Q56 28 42 22" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.5"/>
                <path d="M40 22 Q34 14 42 10 Q50 8 51 18 Q46 19 40 22" fill="currentColor" opacity="0.75"/>
                <path d="M52 18 Q48 9 58 6 Q68 3 67 14 Q60 16 52 18" fill="currentColor" opacity="0.8"/>
                <path d="M68 14 Q66 5 76 3 Q86 2 84 14 Q76 15 68 14" fill="currentColor" opacity="0.85"/>
                <path d="M40 22 Q32 20 30 26 Q28 34 38 32 Q40 27 40 22" fill="currentColor" opacity="0.55"/>
                <path d="M50 30 Q42 30 41 38 Q40 46 50 44 Q51 37 50 30" fill="currentColor" opacity="0.6"/>
                <path d="M64 38 Q56 38 55 46 Q54 54 64 52 Q65 45 64 38" fill="currentColor" opacity="0.7"/>
              </g>
            </svg>
          </div>

          <span className="eyebrow">Call Center Intelligence</span>
          <h1>
            Train an AI <em>ambassador</em><br/>
            from the calls you've already made.
          </h1>
          <p className="hero-sub">
            Upload your call transcripts and recordings. Ambassador learns your tone, your policies, and your answers — then handles your customers' questions with the precision of a seasoned agent.
          </p>

          <div className="hero-ctas">
            <Link to="/login" className="btn-primary">
              Get Started
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
              </svg>
            </Link>
            <a href="#how" className="btn-secondary">See How It Works</a>
          </div>

          <div className="hero-meta">
            <div className="hero-meta-item">
              <strong>4.3<span style={{color: 'var(--gold)'}}>★</span></strong>
              <span>Avg. response rating</span>
            </div>
            <div className="hero-meta-divider"/>
            <div className="hero-meta-item">
              <strong>1,284</strong>
              <span>Calls processed monthly</span>
            </div>
            <div className="hero-meta-divider"/>
            <div className="hero-meta-item">
              <strong>72%</strong>
              <span>Tier-1 questions auto-resolved</span>
            </div>
          </div>
        </div>
      </header>

      {/* ── HOW IT WORKS ── */}
      <section id="how">
        <div className="container">
          <div className="section-head">
            <span className="eyebrow">The Method</span>
            <h2>From Transcripts to Trusted Answers</h2>
            <div className="meander-divider" style={{margin: '22px auto'}}/>
            <p>Three deliberate steps. No prompt engineering. No hallucinated policies. Your call history is your knowledge base.</p>
          </div>

          <div className="steps">
            <div className="step">
              <div className="step-num">I</div>
              <div className="step-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <h3>Upload</h3>
              <p>Drop in transcripts as text, paste them in manually, or submit raw audio for automatic transcription. We handle the messy parts.</p>
            </div>
            <div className="step">
              <div className="step-num">II</div>
              <div className="step-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4L7 17M17 7l1.4-1.4"/>
                </svg>
              </div>
              <h3>Train</h3>
              <p>Ambassador studies your past calls — the questions, the answers, the resolutions — and builds a knowledge model grounded in what your team actually says.</p>
            </div>
            <div className="step">
              <div className="step-num">III</div>
              <div className="step-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
              </div>
              <h3>Deploy</h3>
              <p>Embed the chatbot, monitor every exchange, rate the answers, and approve corrections. The model improves with every conversation.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section className="features-section" id="features">
        <div className="container">
          <div className="section-head">
            <span className="eyebrow">The Apparatus</span>
            <h2>Built for the People Who Actually Run It</h2>
            <div className="meander-divider" style={{margin: '22px auto'}}/>
            <p>Every feature was designed with supervisors, trainers, and quality teams in mind — not engineers.</p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-card-head">
                <div className="feature-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                    <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
                  </svg>
                </div>
                <div>
                  <h3>Audio Transcription</h3>
                  <p>Upload .mp3 or .wav recordings in any of your supported languages. Accurate, editable, ready in seconds.</p>
                </div>
              </div>
            </div>

            <div className="feature-card">
              <div className="feature-card-head">
                <div className="feature-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                  </svg>
                </div>
                <div>
                  <h3>Response Ratings</h3>
                  <p>Every answer is scorable. Track averages, distributions, and trends to find weak spots before customers do.</p>
                </div>
              </div>
            </div>

            <div className="feature-card">
              <div className="feature-card-head">
                <div className="feature-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                </div>
                <div>
                  <h3>Issue Tracking</h3>
                  <p>Flag inaccurate responses. Assign severity, follow status, and document resolution — without leaving the panel.</p>
                </div>
              </div>
            </div>

            <div className="feature-card">
              <div className="feature-card-head">
                <div className="feature-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                  </svg>
                </div>
                <div>
                  <h3>Training Dataset</h3>
                  <p>Approve, reject, or rewrite suggested corrections. Every accepted answer becomes part of the next training cycle.</p>
                </div>
              </div>
            </div>

            <div className="feature-card">
              <div className="feature-card-head">
                <div className="feature-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
                  </svg>
                </div>
                <div>
                  <h3>Live Dashboard</h3>
                  <p>Average ratings, recent activity, rating distribution, and issue counts — at a glance, kept current.</p>
                </div>
              </div>
            </div>

            <div className="feature-card">
              <div className="feature-card-head">
                <div className="feature-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                </div>
                <div>
                  <h3>Role-Based Access</h3>
                  <p>Admins assign roles after sign-up. Agents, supervisors, and quality reviewers each see what they need — nothing more.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── PRODUCT PREVIEW ── */}
      <section className="preview-section">
        <div className="container">
          <div className="section-head">
            <span className="eyebrow">In Conversation</span>
            <h2>Trained on Your Calls. Speaks Like Your Team.</h2>
            <div className="meander-divider" style={{margin: '22px auto'}}/>
            <p>An exchange from a freshly-deployed Ambassador, answering on behalf of a logistics provider.</p>
          </div>

          <div className="preview-frame">
            <div className="preview-header">
              <div className="preview-header-title">AMBASSADOR</div>
              <div className="preview-header-sub">Imperial Call Center Intelligence</div>
            </div>
            <div className="preview-body">
              <div className="msg user">My package is two days late. What can you do?</div>
              <div className="ai-row">
                <div className="ai-coin">A</div>
                <div className="msg ai">
                  <div className="msg-label">Ambassador</div>
                  I see your shipment — order #4921 — left our partner facility on May 4th but is currently held at the regional sorting hub. I've flagged it for priority release. You should see movement within 24 hours, and if it doesn't update by tomorrow evening, I'll authorize a credit for the delay.
                </div>
              </div>
              <div className="msg user">How long do I usually wait for a refund after I return something?</div>
              <div className="ai-row">
                <div className="ai-coin">A</div>
                <div className="msg ai">
                  <div className="msg-label">Ambassador</div>
                  Refunds are processed within 5–7 business days from the moment the warehouse confirms receipt of the returned item. I can send you a tracking link for your return so you'll know the moment it arrives.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── USE CASES ── */}
      <section
        id="usecases"
        style={{background: 'var(--paper-deep)', borderTop: '1px solid var(--line)', borderBottom: '1px solid var(--line)'}}
      >
        <div className="container">
          <div className="section-head">
            <span className="eyebrow">Where It Serves</span>
            <h2>One Platform, Many Operations</h2>
            <div className="meander-divider" style={{margin: '22px auto'}}/>
          </div>

          <div className="usecases" style={{background: '#fff'}}>
            <div className="usecase">
              <div className="usecase-num">I.</div>
              <h3>Customer Support</h3>
              <p>Resolve refund inquiries, order tracking, and account questions instantly — using the exact language your team has refined over thousands of calls.</p>
            </div>
            <div className="usecase">
              <div className="usecase-num">II.</div>
              <h3>Internal Helpdesk</h3>
              <p>Train Ambassador on internal SOPs, escalation paths, and product documentation. New agents get instant, accurate answers on demand.</p>
            </div>
            <div className="usecase">
              <div className="usecase-num">III.</div>
              <h3>Quality Assurance</h3>
              <p>Surface inconsistent agent responses, flag policy drift, and feed corrections back into the model — closing the QA loop in one place.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── QUOTE ── */}
      <section className="quote-section">
        <div className="container">
          <div className="quote-mark">"</div>
          <p className="quote-text">
            We trained Ambassador on six months of recorded calls. Within two weeks it was answering tier-one questions better than half our new hires.
          </p>
          <div className="quote-attr">— TARIK FETAHOVIĆ</div>
          <div className="quote-attr-sub">Head of Customer Operations, Sarajevo Logistics</div>
        </div>
      </section>

      {/* ── FINAL CTA ── */}
      <section className="cta-section">
        <div className="container">
          <span className="eyebrow">Begin</span>
          <h2>Your Best Agents Have Already Written the Script.</h2>
          <p>Let Ambassador read it, learn it, and answer in their voice. Set up takes minutes — not weeks.</p>
          <Link to="/login" className="btn-primary" style={{fontSize: '14px', padding: '15px 36px'}}>
            Sign In or Create an Account
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </Link>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer>
        <div className="footer-inner">
          <div className="footer-logo">
            <svg width="22" height="14" viewBox="0 0 90 50" fill="none" style={{color: 'var(--gold)'}}>
              <path d="M44 42 Q38 36 30 30 Q20 22 12 18" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.5"/>
              <path d="M12 18 Q8 12 14 8 Q20 6 21 14 Q17 15 12 18" fill="currentColor" opacity="0.7"/>
              <path d="M22 14 Q20 7 27 5 Q34 3 34 12 Q29 13 22 14" fill="currentColor" opacity="0.75"/>
              <path d="M34 11 Q34 4 41 3 Q48 2 47 11 Q42 12 34 11" fill="currentColor" opacity="0.85"/>
            </svg>
            AMBASSADOR
          </div>
          <div className="footer-links">
            <a href="#how">How it works</a>
            <a href="#features">Features</a>
            <a href="#usecases">Use cases</a>
            <Link to="/login">Sign In</Link>
            <a href="#">Contact</a>
            <a href="#">Privacy</a>
          </div>
          <div className="footer-copy">© 2026 Ambassador · Imperial Call Center Intelligence</div>
        </div>
      </footer>

    </div>
  );
}
