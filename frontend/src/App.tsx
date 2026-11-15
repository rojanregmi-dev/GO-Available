import { HostedSignIn } from "./components/HostedSignIn";

export default function App() {
  return (
    <main className="app-shell-signin">
      <header className="signin-brand">
        <img
          className="signin-hero"
          src="/go-available-activities.jpg"
          alt=""
          width="1080"
          height="1350"
        />
        <h1>GO <span>AVAILABLE</span></h1>
        <div className="signin-intro">
          <p className="signin-tagline">Your time.<br />More possibilities.</p>
          <p>Find people and plans that fit your free time.</p>
        </div>
      </header>
      <HostedSignIn />
    </main>
  );
}
