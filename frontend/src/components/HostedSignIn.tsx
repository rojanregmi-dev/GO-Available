import { useEffect, useState, type FormEvent } from "react";
import type { User } from "@supabase/supabase-js";
import { authClient } from "../lib/auth";

export function HostedSignIn() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(Boolean(authClient));
  const [isSigningUp, setIsSigningUp] = useState(false);
  const [pending, setPending] = useState<"email" | "google" | "sign-out" | null>(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const busy = pending !== null;

  useEffect(() => {
    if (!authClient) return;

    const { data: { subscription } } = authClient.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
        setLoading(false);
      },
    );
    let active = true;
    void authClient.auth.initialize().then(({ error }) => {
      if (active && error) {
        setError("We couldn’t finish signing you in. Please try again.");
      }
    });

    return () => {
      active = false;
      subscription.unsubscribe();
    };
  }, []);

  function changeMode(signUp: boolean) {
    setIsSigningUp(signUp);
    setError("");
    setMessage("");
  }

  async function emailSignIn(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!authClient || busy) return;

    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") ?? "").trim();
    const displayName = String(form.get("displayName") ?? "").trim();
    setError("");
    setMessage("");
    if (isSigningUp && !displayName) {
      setError("Enter the name you want to use on GO Available.");
      return;
    }

    setPending("email");
    try {
      const { error } = await authClient.auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: window.location.origin + "/",
          shouldCreateUser: isSigningUp,
          ...(isSigningUp ? { data: { display_name: displayName } } : {}),
        },
      });
      if (error) throw error;
      setMessage("Check your email for a link to continue.");
    } catch {
      setError("We couldn’t send a link. Check your email address and try again.");
    } finally {
      setPending(null);
    }
  }

  async function googleSignIn() {
    if (!authClient || busy) return;
    setPending("google");
    setError("");
    setMessage("");
    const { error } = await authClient.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: window.location.origin + "/" },
    });
    if (error) {
      setError("We couldn’t open Google sign-in. Please try again.");
      setPending(null);
    }
  }

  async function signOut() {
    if (!authClient || busy) return;
    setPending("sign-out");
    setError("");
    setMessage("");
    const { error } = await authClient.auth.signOut({ scope: "local" });
    if (error) setError("We couldn’t sign you out. Please try again.");
    setPending(null);
  }

  return (
    <section className="signin-card" aria-labelledby="sign-in-heading">
      <h2 id="sign-in-heading">
        {user ? "You’re signed in" : isSigningUp ? "Create your account" : "Sign in"}
      </h2>
      {loading ? (
        <p role="status">Checking session…</p>
      ) : user ? (
        <>
          {user.email && <p className="signin-detail">{user.email}</p>}
          <button type="button" onClick={signOut} disabled={busy}>Sign out</button>
        </>
      ) : (
        <>
          <div className="signin-mode" role="group" aria-label="Account options">
            <button type="button" aria-pressed={!isSigningUp} onClick={() => changeMode(false)} disabled={busy}>
              Sign in
            </button>
            <button type="button" aria-pressed={isSigningUp} onClick={() => changeMode(true)} disabled={busy}>
              Sign up
            </button>
          </div>
          <button className="signin-google" type="button" onClick={googleSignIn} disabled={!authClient || busy}>
            <img src="/google-g.png" alt="" width="18" height="18" />
            {pending === "google" ? "Opening Google…" : "Continue with Google"}
          </button>
          <p className="signin-divider">or use email</p>
          <form className="signin-form" onSubmit={emailSignIn}>
            {isSigningUp && (
              <label htmlFor="account-name">
                Account name
                <input id="account-name" name="displayName" autoComplete="name" maxLength={100} required />
              </label>
            )}
            <label htmlFor="account-email">
              Email address
              <input id="account-email" name="email" type="email" autoComplete="email" required />
            </label>
            <button type="submit" disabled={!authClient || busy}>
              {pending === "email" ? "Sending…" : isSigningUp ? "Send account link" : "Send sign-in link"}
            </button>
          </form>
          {message && <p className="signin-detail" role="status">{message}</p>}
        </>
      )}
      {!authClient && <p role="alert">Sign-in is currently unavailable.</p>}
      {error && <p role="alert">{error}</p>}
    </section>
  );
}
