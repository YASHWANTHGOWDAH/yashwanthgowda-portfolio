import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowUpRight, Github, Linkedin, Mail, Download, Menu, X,
  Code2, BrainCircuit, Database, Terminal, GraduationCap,
  ExternalLink, ChevronDown
} from "lucide-react";
import "./styles.css";

const githubUrl = "https://github.com/YASHWANTHGOWDAH";
const linkedinUrl = "https://www.linkedin.com/in/yashwanth-gowda-h-296505304/";

const skills = [
  { name: "Python", icon: Terminal },
  { name: "Java", icon: Code2 },
  { name: "C", icon: Code2 },
  { name: "SQL", icon: Database },
  { name: "AI / ML", icon: BrainCircuit },
  { name: "DSA", icon: Code2 },
  { name: "OOP", icon: Code2 },
  { name: "DBMS", icon: Database },
];

const projects = [
  {
    number: "01",
    title: "Trading Bot With Machine Learning",
    status: "Ongoing",
    description:
      "An AI-powered trading system that analyzes historical and real-time stock-market data to generate BUY, SELL, and HOLD signals.",
    tech: ["Python", "Pandas", "NumPy", "Random Forest", "Machine Learning"],
  },
  {
    number: "02",
    title: "Offline Cloud Data Retrieval Interface",
    status: "Mini Project",
    description:
      "A self-hosted offline file-management system with a Flask backend, browser interface, local metadata database, uploads, descriptions, and fast search.",
    tech: ["Python", "Flask", "Database", "HTML", "CSS", "JavaScript"],
  },
];

const certifications = [
  ["2026", "Building RAG Apps Using MongoDB"],
  ["2025", "The Bits and Bytes of Computer Networking"],
  ["2025", "Artificial Intelligence Fundamentals — IBM SkillsBuild"],
];

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const closeMenu = () => setMenuOpen(false);

  return (
    <div className="site">
      <div className="noise" />
      <div className="orb orb-a" />
      <div className="orb orb-b" />

      <header className={scrolled ? "nav scrolled" : "nav"}>
        <a className="brand" href="#home" onClick={closeMenu}>
          YGH<span>.</span>
        </a>

        <nav className={menuOpen ? "nav-links open" : "nav-links"}>
          {["home", "about", "skills", "projects", "education", "contact"].map((item) => (
            <a key={item} href={`#${item}`} onClick={closeMenu}>
              {item}
            </a>
          ))}
        </nav>

        <div className="nav-actions">
          <a className="nav-social" href={githubUrl} target="_blank" rel="noreferrer" aria-label="GitHub">
            <Github size={18} />
          </a>
          <a className="nav-social" href={linkedinUrl} target="_blank" rel="noreferrer" aria-label="LinkedIn">
            <Linkedin size={18} />
          </a>
          <button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)} aria-label="Menu">
            {menuOpen ? <X /> : <Menu />}
          </button>
        </div>
      </header>

      <main>
        <section id="home" className="hero section">
          <div className="hero-copy reveal">
            <p className="eyebrow"><span className="dot" /> Available for opportunities</p>
            <h1>
              Hi, I'm <span>Yashwanth</span>.
              <br />
              I build <em>intelligent</em> software.
            </h1>
            <p className="hero-text">
              Information Science & Engineering student focused on software development,
              problem-solving, and Machine Learning.
            </p>

            <div className="hero-buttons">
              <a className="btn primary" href="#projects">
                Explore my work <ArrowUpRight size={18} />
              </a>
              <a className="btn ghost" href="/Yashwanth_Gowda_Resume.pdf" download>
                Resume <Download size={17} />
              </a>
            </div>

            <div className="social-row">
              <a href={githubUrl} target="_blank" rel="noreferrer"><Github size={18}/> GitHub</a>
              <a href={linkedinUrl} target="_blank" rel="noreferrer"><Linkedin size={18}/> LinkedIn</a>
            </div>
          </div>

          <div className="hero-visual reveal delay">
            <div className="portrait-frame">
              <div className="portrait-glow" />
              <img src="/profile.jpg" alt="Yashwanth Gowda H" />
              <div className="portrait-tag">Software Engineer · ML</div>
            </div>
            <div className="floating-card card-one">
              <span>01</span><b>Python</b>
            </div>
            <div className="floating-card card-two">
              <span>02</span><b>Machine Learning</b>
            </div>
          </div>

          <a className="scroll-cue" href="#about">
            <span>Scroll to explore</span><ChevronDown size={18}/>
          </a>
        </section>

        <section id="about" className="section split-section">
          <div className="section-label">01 / About</div>
          <div className="section-content">
            <p className="kicker">A developer in progress</p>
            <h2>Curious by nature.<br /><span>Focused on building.</span></h2>
            <p className="body-copy">
              I'm an Information Science & Engineering student at Sai Vidya Institute of
              Technology, Bengaluru. I enjoy turning ideas into practical software and
              exploring how Machine Learning can solve real-world problems.
            </p>
            <p className="body-copy">
              My foundation includes programming, Data Structures & Algorithms, OOP,
              Operating Systems, DBMS, and computer networks. I'm currently developing
              an ML-powered trading bot and strengthening my software-engineering skills.
            </p>

            <div className="facts">
              <div><strong>7.3</strong><small>CGPA / 10</small></div>
              <div><strong>2027</strong><small>Expected graduation</small></div>
              <div><strong>2+</strong><small>Featured projects</small></div>
            </div>
          </div>
        </section>

        <section id="skills" className="section">
          <div className="section-label">02 / Skills</div>
          <div className="section-content wide">
            <p className="kicker">Technical toolkit</p>
            <h2>Tools I use to<br /><span>turn ideas into code.</span></h2>
            <div className="skills-grid">
              {skills.map(({ name, icon: Icon }) => (
                <div className="skill-card" key={name}>
                  <Icon size={22} />
                  <span>{name}</span>
                </div>
              ))}
            </div>
            <div className="skill-note">
              <span>Core focus</span>
              <p>Software Development · AI/ML · Data Structures & Algorithms · Problem Solving</p>
            </div>
          </div>
        </section>

        <section id="projects" className="section">
          <div className="section-label">03 / Projects</div>
          <div className="section-content wide">
            <div className="section-heading-row">
              <div>
                <p className="kicker">Selected work</p>
                <h2>Projects that show<br /><span>how I think.</span></h2>
              </div>
              <a className="text-link" href={githubUrl} target="_blank" rel="noreferrer">
                View GitHub <ExternalLink size={16}/>
              </a>
            </div>

            <div className="projects">
              {projects.map((project) => (
                <article className="project" key={project.number}>
                  <div className="project-number">{project.number}</div>
                  <div className="project-main">
                    <div className="project-meta">{project.status}</div>
                    <h3>{project.title}</h3>
                    <p>{project.description}</p>
                    <div className="tags">
                      {project.tech.map((tag) => <span key={tag}>{tag}</span>)}
                    </div>
                  </div>
                  <div className="project-arrow"><ArrowUpRight /></div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="education" className="section">
          <div className="section-label">04 / Education</div>
          <div className="section-content wide">
            <p className="kicker">Academic journey</p>
            <h2>Learning the fundamentals<br /><span>and going beyond them.</span></h2>

            <div className="education-card">
              <div className="edu-icon"><GraduationCap size={28}/></div>
              <div>
                <p className="project-meta">Sep 2023 — Sep 2027</p>
                <h3>Bachelor of Engineering — Information Science & Engineering</h3>
                <p>Sai Vidya Institute of Technology, Rajanukunte, Bengaluru</p>
              </div>
              <div className="edu-score"><strong>7.3</strong><small>CGPA</small></div>
            </div>

            <div className="education-card secondary">
              <div className="edu-icon"><GraduationCap size={24}/></div>
              <div>
                <p className="project-meta">Jun 2021 — May 2023</p>
                <h3>Pre-University College — Science (PCMB)</h3>
                <p>Dhanwanthri PU College, Bengaluru</p>
              </div>
              <div className="edu-score"><strong>75.6%</strong><small>Percentage</small></div>
            </div>

            <div className="certs">
              <p className="kicker">Certifications</p>
              {certifications.map(([year, name]) => (
                <div className="cert-row" key={name}>
                  <span>{year}</span><b>{name}</b><ArrowUpRight size={16}/>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="contact" className="contact section">
          <div className="contact-inner">
            <p className="kicker">05 / Contact</p>
            <h2>Let's build something<br /><span>worth talking about.</span></h2>
            <p>I'm open to software-engineering opportunities, internships, collaborations, and interesting projects.</p>
            <div className="contact-buttons">
              <a className="btn primary" href={linkedinUrl} target="_blank" rel="noreferrer">
                Connect on LinkedIn <Linkedin size={18}/>
              </a>
              <a className="btn ghost" href={githubUrl} target="_blank" rel="noreferrer">
                Visit GitHub <Github size={18}/>
              </a>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <span>© {new Date().getFullYear()} Yashwanth Gowda H</span>
        <span>Bengaluru, India</span>
        <a href="#home">Back to top ↑</a>
      </footer>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
