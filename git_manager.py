import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import json
import os
import sys

# ── colour palette ──────────────────────────────────────────────
BG        = "#0d1117"
PANEL     = "#161b22"
BORDER    = "#30363d"
ACCENT    = "#238636"
ACCENT_H  = "#2ea043"
DANGER    = "#da3633"
DANGER_H  = "#f85149"
BLUE      = "#1f6feb"
BLUE_H    = "#388bfd"
TEXT      = "#e6edf3"
MUTED     = "#8b949e"
YELLOW    = "#d29922"
WHITE     = "#ffffff"

FONT_TITLE  = ("Consolas", 20, "bold")
FONT_HEAD   = ("Consolas", 11, "bold")
FONT_BODY   = ("Consolas", 10)
FONT_SMALL  = ("Consolas", 9)
FONT_BADGE  = ("Consolas", 8, "bold")

PROFILES_FILE = os.path.join(os.path.expanduser("~"), ".git_manager_profiles.json")

# ── Git helpers ──────────────────────────────────────────────────
def run_git(*args):
    try:
        r = subprocess.run(
            ["git"] + list(args),
            capture_output=True, text=True
        )
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except FileNotFoundError:
        return "", "git not found", 1

def get_global(key):
    out, _, rc = run_git("config", "--global", key)
    return out if rc == 0 else ""

def set_global(key, value):
    _, err, rc = run_git("config", "--global", key, value)
    return rc == 0, err

def get_all_globals():
    out, _, _ = run_git("config", "--global", "--list")
    cfg = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            cfg[k] = v
    return cfg

def list_credential_helpers():
    out, _, _ = run_git("config", "--global", "--get-all", "credential.helper")
    return [x for x in out.splitlines() if x.strip()]

# ── Profile store ────────────────────────────────────────────────
def load_profiles():
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

# ════════════════════════════════════════════════════════════════
class GitManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Git Manager")
        self.geometry("900x680")
        self.minsize(780, 580)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.profiles = load_profiles()
        self.active_profile = None

        self._build_ui()
        self.refresh_all()

    # ── Layout ─────────────────────────────────────────────────
    def _build_ui(self):
        # Title bar
        hdr = tk.Frame(self, bg=BG, pady=0)
        hdr.pack(fill="x", padx=0)

        tk.Label(hdr, text="⬡  GIT MANAGER", font=FONT_TITLE,
                 bg=BG, fg=ACCENT).pack(side="left", padx=24, pady=14)

        self.status_lbl = tk.Label(hdr, text="", font=FONT_SMALL, bg=BG, fg=MUTED)
        self.status_lbl.pack(side="right", padx=24)

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x")

        # Notebook tabs
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0, tabmargins=0)
        style.configure("TNotebook.Tab",
                        background=PANEL, foreground=MUTED,
                        font=FONT_HEAD, padding=[18, 8],
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG)],
                  foreground=[("selected", TEXT)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_profiles  = tk.Frame(nb, bg=BG)
        self.tab_globals   = tk.Frame(nb, bg=BG)
        self.tab_creds     = tk.Frame(nb, bg=BG)

        nb.add(self.tab_profiles, text="  Profiles  ")
        nb.add(self.tab_globals,  text="  Global Config  ")
        nb.add(self.tab_creds,    text="  Credential Helpers  ")

        self._build_profiles_tab()
        self._build_globals_tab()
        self._build_creds_tab()

    # ════════════════════════════════════════════════════════════
    # TAB 1 – Profiles
    # ════════════════════════════════════════════════════════════
    def _build_profiles_tab(self):
        t = self.tab_profiles
        t.columnconfigure(0, weight=1)
        t.rowconfigure(1, weight=1)

        # Top bar
        bar = tk.Frame(t, bg=BG)
        bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))

        tk.Label(bar, text="Saved Git Accounts", font=FONT_HEAD,
                 bg=BG, fg=TEXT).pack(side="left")

        self._btn(bar, "+ Add Account", self._add_profile,
                  ACCENT, ACCENT_H).pack(side="right")

        # Profile list
        list_frame = tk.Frame(t, bg=BG)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        list_frame.columnconfigure(0, weight=1)

        self.profile_canvas = tk.Canvas(list_frame, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(list_frame, orient="vertical",
                          command=self.profile_canvas.yview)
        self.profile_canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.profile_canvas.pack(side="left", fill="both", expand=True)

        self.profile_inner = tk.Frame(self.profile_canvas, bg=BG)
        self.profile_canvas.create_window((0, 0), window=self.profile_inner,
                                          anchor="nw", tags="inner")
        self.profile_inner.bind("<Configure>",
            lambda e: self.profile_canvas.configure(
                scrollregion=self.profile_canvas.bbox("all")))
        self.profile_canvas.bind("<Configure>",
            lambda e: self.profile_canvas.itemconfig(
                "inner", width=e.width))

        # Active profile footer
        footer = tk.Frame(t, bg=PANEL, pady=10)
        footer.grid(row=2, column=0, sticky="ew", padx=0)

        tk.Label(footer, text="ACTIVE:", font=FONT_BADGE,
                 bg=PANEL, fg=MUTED).pack(side="left", padx=(20, 6))
        self.active_lbl = tk.Label(footer, text="(none)", font=FONT_BODY,
                                   bg=PANEL, fg=YELLOW)
        self.active_lbl.pack(side="left")

        self.current_lbl = tk.Label(footer, text="", font=FONT_SMALL,
                                    bg=PANEL, fg=MUTED)
        self.current_lbl.pack(side="right", padx=20)

    def _render_profiles(self):
        for w in self.profile_inner.winfo_children():
            w.destroy()

        current_name  = get_global("user.name")
        current_email = get_global("user.email")

        if not self.profiles:
            tk.Label(self.profile_inner,
                     text="No profiles saved yet.\nClick '+ Add Account' to get started.",
                     font=FONT_BODY, bg=BG, fg=MUTED,
                     justify="center").pack(pady=40)
            return

        for i, p in enumerate(self.profiles):
            is_active = (p["name"] == current_name and
                         p["email"] == current_email)
            self._profile_card(self.profile_inner, p, i, is_active)

        self.current_lbl.config(
            text=f"git: {current_name} <{current_email}>" if current_name else "No git user set"
        )

    def _profile_card(self, parent, profile, idx, is_active):
        card = tk.Frame(parent, bg=PANEL,
                        highlightbackground=ACCENT if is_active else BORDER,
                        highlightthickness=1 if is_active else 1,
                        cursor="hand2")
        card.pack(fill="x", pady=4, padx=2)
        card.columnconfigure(1, weight=1)

        # Indicator
        dot_color = ACCENT if is_active else BORDER
        dot = tk.Frame(card, bg=dot_color, width=4)
        dot.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 12))

        tk.Label(card, text=profile["name"], font=FONT_HEAD,
                 bg=PANEL, fg=WHITE if is_active else TEXT,
                 anchor="w").grid(row=0, column=1, sticky="w", padx=(0, 8), pady=(10, 2))

        tk.Label(card, text=profile["email"], font=FONT_SMALL,
                 bg=PANEL, fg=MUTED, anchor="w"
                 ).grid(row=1, column=1, sticky="w", padx=(0, 8), pady=(0, 10))

        if profile.get("token_hint"):
            tk.Label(card, text=f"Token: {profile['token_hint']}",
                     font=FONT_SMALL, bg=PANEL, fg=MUTED
                     ).grid(row=0, column=2, rowspan=2, padx=8)

        # Buttons
        btn_frame = tk.Frame(card, bg=PANEL)
        btn_frame.grid(row=0, column=3, rowspan=2, padx=10, pady=6)

        if is_active:
            tk.Label(btn_frame, text="✓ ACTIVE", font=FONT_BADGE,
                     bg=PANEL, fg=ACCENT).pack(side="left", padx=(0, 6))
        else:
            self._btn(btn_frame, "Apply", lambda p=profile: self._apply_profile(p),
                      BLUE, BLUE_H, pad=(6, 4)).pack(side="left", padx=(0, 4))

        self._btn(btn_frame, "Edit", lambda i=idx: self._edit_profile(i),
                  PANEL, BORDER, pad=(6, 4)).pack(side="left", padx=(0, 4))
        self._btn(btn_frame, "✕", lambda i=idx: self._delete_profile(i),
                  PANEL, DANGER, pad=(6, 4), fg=DANGER).pack(side="left")

    def _apply_profile(self, profile):
        ok1, e1 = set_global("user.name",  profile["name"])
        ok2, e2 = set_global("user.email", profile["email"])
        errs = []
        if not ok1: errs.append(e1)
        if not ok2: errs.append(e2)
        if errs:
            messagebox.showerror("Error", "\n".join(errs))
        else:
            self.active_lbl.config(text=profile["name"])
            self._flash(f"✓ Switched to {profile['name']}")
            self.refresh_all()

    def _add_profile(self):
        dlg = ProfileDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            self.profiles.append(dlg.result)
            save_profiles(self.profiles)
            self.refresh_all()

    def _edit_profile(self, idx):
        dlg = ProfileDialog(self, existing=self.profiles[idx])
        self.wait_window(dlg)
        if dlg.result:
            self.profiles[idx] = dlg.result
            save_profiles(self.profiles)
            self.refresh_all()

    def _delete_profile(self, idx):
        name = self.profiles[idx]["name"]
        if messagebox.askyesno("Delete Profile", f"Remove '{name}'?"):
            self.profiles.pop(idx)
            save_profiles(self.profiles)
            self.refresh_all()

    # ════════════════════════════════════════════════════════════
    # TAB 2 – Global Config
    # ════════════════════════════════════════════════════════════
    def _build_globals_tab(self):
        t = self.tab_globals
        t.columnconfigure(0, weight=1)
        t.rowconfigure(1, weight=1)

        bar = tk.Frame(t, bg=BG)
        bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))
        tk.Label(bar, text="Global Git Config  (~/.gitconfig)", font=FONT_HEAD,
                 bg=BG, fg=TEXT).pack(side="left")
        self._btn(bar, "⟳ Refresh", self.refresh_all, PANEL, BORDER).pack(side="right")
        self._btn(bar, "+ Add Key", self._add_config_key, BLUE, BLUE_H).pack(side="right", padx=(0, 8))

        # Treeview
        cols = ("Key", "Value")
        frame = tk.Frame(t, bg=BG)
        frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=4)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=PANEL, foreground=TEXT,
                        fieldbackground=PANEL, rowheight=28,
                        font=FONT_BODY, borderwidth=0)
        style.configure("Dark.Treeview.Heading",
                        background=BORDER, foreground=MUTED,
                        font=FONT_SMALL, relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", BLUE)],
                  foreground=[("selected", WHITE)])

        self.cfg_tree = ttk.Treeview(frame, columns=cols, show="headings",
                                     style="Dark.Treeview")
        self.cfg_tree.heading("Key",   text="Key",   anchor="w")
        self.cfg_tree.heading("Value", text="Value", anchor="w")
        self.cfg_tree.column("Key",   width=280, stretch=False)
        self.cfg_tree.column("Value", width=400, stretch=True)

        vsb = tk.Scrollbar(frame, orient="vertical", command=self.cfg_tree.yview)
        self.cfg_tree.configure(yscrollcommand=vsb.set)
        self.cfg_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.cfg_tree.bind("<Double-1>", self._edit_config_row)

        # Quick-set bar
        quick = tk.Frame(t, bg=PANEL, pady=8)
        quick.grid(row=2, column=0, sticky="ew")
        tk.Label(quick, text="Quick set:", font=FONT_BADGE,
                 bg=PANEL, fg=MUTED).pack(side="left", padx=(20, 8))

        quick_items = [
            ("user.name",  "Name"),
            ("user.email", "Email"),
            ("core.editor","Editor"),
        ]
        for key, label in quick_items:
            self._btn(quick, label,
                      lambda k=key: self._quick_set(k),
                      PANEL, BORDER, pad=(6, 4)).pack(side="left", padx=4)

    def _render_globals(self):
        self.cfg_tree.delete(*self.cfg_tree.get_children())
        cfg = get_all_globals()
        for k, v in sorted(cfg.items()):
            tag = "user" if k.startswith("user.") else ("core" if k.startswith("core.") else "other")
            self.cfg_tree.insert("", "end", values=(k, v), tags=(tag,))
        self.cfg_tree.tag_configure("user", foreground=YELLOW)
        self.cfg_tree.tag_configure("core", foreground=BLUE_H)
        self.cfg_tree.tag_configure("other", foreground=TEXT)

    def _edit_config_row(self, event):
        sel = self.cfg_tree.selection()
        if not sel:
            return
        key, val = self.cfg_tree.item(sel[0])["values"]
        new_val = simpledialog.askstring("Edit Config",
                                         f"New value for  {key}:",
                                         initialvalue=val,
                                         parent=self)
        if new_val is not None:
            ok, err = set_global(key, new_val)
            if ok:
                self._flash(f"✓ {key} updated")
                self._render_globals()
            else:
                messagebox.showerror("Error", err)

    def _quick_set(self, key):
        cur = get_global(key)
        new_val = simpledialog.askstring("Quick Set",
                                          f"{key}:",
                                          initialvalue=cur,
                                          parent=self)
        if new_val is not None:
            ok, err = set_global(key, new_val)
            if ok:
                self._flash(f"✓ {key} = {new_val}")
                self.refresh_all()
            else:
                messagebox.showerror("Error", err)

    def _add_config_key(self):
        key = simpledialog.askstring("Add Config Key", "Key (e.g. core.autocrlf):", parent=self)
        if not key:
            return
        val = simpledialog.askstring("Add Config Value", f"Value for  {key}:", parent=self)
        if val is not None:
            ok, err = set_global(key, val)
            if ok:
                self._flash(f"✓ Added {key}")
                self._render_globals()
            else:
                messagebox.showerror("Error", err)

    # ════════════════════════════════════════════════════════════
    # TAB 3 – Credential Helpers
    # ════════════════════════════════════════════════════════════
    def _build_creds_tab(self):
        t = self.tab_creds
        t.columnconfigure(0, weight=1)
        t.rowconfigure(1, weight=1)

        bar = tk.Frame(t, bg=BG)
        bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))
        tk.Label(bar, text="Credential Helpers & Login Tokens", font=FONT_HEAD,
                 bg=BG, fg=TEXT).pack(side="left")

        info = tk.Frame(t, bg=PANEL, padx=20, pady=14)
        info.grid(row=1, column=0, sticky="nsew", padx=20, pady=4)
        info.columnconfigure(0, weight=1)
        info.rowconfigure(3, weight=1)

        # Current helper
        tk.Label(info, text="credential.helper", font=FONT_HEAD,
                 bg=PANEL, fg=MUTED).grid(row=0, column=0, sticky="w")
        self.helper_lbl = tk.Label(info, text="", font=FONT_BODY,
                                   bg=PANEL, fg=TEXT, anchor="w")
        self.helper_lbl.grid(row=1, column=0, sticky="w", pady=(2, 14))

        tk.Label(info, text="Set credential helper:", font=FONT_HEAD,
                 bg=PANEL, fg=MUTED).grid(row=2, column=0, sticky="w")

        helper_frame = tk.Frame(info, bg=PANEL)
        helper_frame.grid(row=3, column=0, sticky="nw", pady=8)

        helpers = [
            ("manager",          "Git Credential Manager (Windows/Mac)", ACCENT),
            ("manager-core",     "Git Credential Manager Core",          ACCENT),
            ("store",            "Store (plaintext ~/.git-credentials)",  YELLOW),
            ("cache",            "Cache (in-memory, 15 min)",             BLUE),
            ("osxkeychain",      "macOS Keychain",                        BLUE_H),
            ("wincred",          "Windows Credential Store",              BLUE_H),
        ]

        for helper, label, color in helpers:
            row = tk.Frame(helper_frame, bg=PANEL)
            row.pack(fill="x", pady=3)
            self._btn(row, "Set", lambda h=helper: self._set_helper(h),
                      PANEL, BORDER, pad=(5, 3)).pack(side="left", padx=(0, 10))
            tk.Label(row, text=f"{helper}", font=("Consolas", 10, "bold"),
                     bg=PANEL, fg=color, width=22, anchor="w").pack(side="left")
            tk.Label(row, text=f"— {label}", font=FONT_SMALL,
                     bg=PANEL, fg=MUTED, anchor="w").pack(side="left")

        # Custom
        custom_frame = tk.Frame(info, bg=PANEL)
        custom_frame.grid(row=4, column=0, sticky="sw", pady=(16, 0))
        tk.Label(custom_frame, text="Custom helper:", font=FONT_SMALL,
                 bg=PANEL, fg=MUTED).pack(side="left", padx=(0, 8))
        self.custom_entry = tk.Entry(custom_frame, font=FONT_BODY,
                                     bg=BORDER, fg=TEXT, insertbackground=TEXT,
                                     relief="flat", width=30)
        self.custom_entry.pack(side="left", padx=(0, 8), ipady=4)
        self._btn(custom_frame, "Apply",
                  lambda: self._set_helper(self.custom_entry.get()),
                  BLUE, BLUE_H, pad=(8, 4)).pack(side="left")

    def _render_creds(self):
        helpers = list_credential_helpers()
        if helpers:
            self.helper_lbl.config(text="  ".join(helpers) or "(none)", fg=TEXT)
        else:
            self.helper_lbl.config(text="(none configured)", fg=MUTED)

    def _set_helper(self, helper):
        if not helper:
            return
        ok, err = set_global("credential.helper", helper)
        if ok:
            self._flash(f"✓ credential.helper = {helper}")
            self._render_creds()
        else:
            messagebox.showerror("Error", err)

    # ── Shared helpers ──────────────────────────────────────────
    def refresh_all(self):
        self._render_profiles()
        self._render_globals()
        self._render_creds()
        # Update active label
        cur = get_global("user.name")
        self.active_lbl.config(text=cur if cur else "(none)")

    def _flash(self, msg):
        self.status_lbl.config(text=msg, fg=ACCENT)
        self.after(3000, lambda: self.status_lbl.config(text=""))

    def _btn(self, parent, text, cmd, bg, hover_bg,
             pad=(10, 6), fg=TEXT, **kw):
        b = tk.Label(parent, text=text, font=FONT_SMALL,
                     bg=bg, fg=fg, cursor="hand2",
                     padx=pad[0], pady=pad[1], relief="flat")
        b.bind("<Button-1>", lambda e: cmd())
        b.bind("<Enter>",    lambda e: b.config(bg=hover_bg, fg=WHITE))
        b.bind("<Leave>",    lambda e: b.config(bg=bg, fg=fg))
        return b


# ════════════════════════════════════════════════════════════════
# Profile Add/Edit Dialog
# ════════════════════════════════════════════════════════════════
class ProfileDialog(tk.Toplevel):
    def __init__(self, parent, existing=None):
        super().__init__(parent)
        self.result = None
        self.title("Edit Account" if existing else "Add Account")
        self.configure(bg=BG)
        self.geometry("460x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Git Account",
                 font=("Consolas", 14, "bold"), bg=BG, fg=TEXT
                 ).pack(pady=(20, 4))

        form = tk.Frame(self, bg=BG)
        form.pack(padx=30, pady=10, fill="x")

        fields = [
            ("Display Name *",   "name",       existing.get("name", "")        if existing else ""),
            ("Email *",          "email",      existing.get("email", "")       if existing else ""),
            ("Token / Password", "token",      existing.get("token", "")       if existing else ""),
            ("Token hint",       "token_hint", existing.get("token_hint", "")  if existing else ""),
        ]

        self.vars = {}
        for row, (label, key, default) in enumerate(fields):
            tk.Label(form, text=label, font=FONT_SMALL, bg=BG, fg=MUTED,
                     anchor="w", width=18).grid(row=row, column=0, pady=5, sticky="w")
            show = "*" if key == "token" else ""
            entry = tk.Entry(form, font=FONT_BODY, bg=PANEL, fg=TEXT,
                             insertbackground=TEXT, relief="flat",
                             show=show, width=28)
            entry.insert(0, default)
            entry.grid(row=row, column=1, pady=5, ipady=5, sticky="ew")
            self.vars[key] = entry

        form.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=16)

        def save():
            name  = self.vars["name"].get().strip()
            email = self.vars["email"].get().strip()
            if not name or not email:
                messagebox.showwarning("Required", "Name and Email are required.", parent=self)
                return
            token      = self.vars["token"].get().strip()
            token_hint = self.vars["token_hint"].get().strip()
            if not token_hint and token:
                token_hint = token[:4] + "****" + token[-2:] if len(token) > 6 else "****"
            self.result = {"name": name, "email": email,
                           "token": token, "token_hint": token_hint}
            self.destroy()

        for text, cmd, bg, hover in [
            ("Save", save, ACCENT, ACCENT_H),
            ("Cancel", self.destroy, PANEL, BORDER),
        ]:
            b = tk.Label(btn_frame, text=text, font=FONT_BODY,
                         bg=bg, fg=TEXT, cursor="hand2",
                         padx=14, pady=7, relief="flat")
            b.bind("<Button-1>", lambda e, c=cmd: c())
            b.bind("<Enter>", lambda e, b=b, h=hover: b.config(bg=h))
            b.bind("<Leave>", lambda e, b=b, bg=bg: b.config(bg=bg))
            b.pack(side="left", padx=6)


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    app = GitManager()
    app.mainloop()