# UI / Tkinter
import tkinter as tk
from tkinter import (
    filedialog,
    messagebox,
    Toplevel,
    Frame,
    Label,
    Entry,
    Button,
    Radiobutton,
    StringVar,
    Text,
    Scrollbar,
    END,
    RIGHT,
    Y,
    LEFT,
    BOTH,
)

# CustomTkinter
import customtkinter as ctk

# Sistema / Utilidades
import os
import json
import subprocess
import webbrowser
import threading
from urllib.parse import urlparse
# Ícone da tray
from pystray import Icon, MenuItem, Menu
# Imagens
from PIL import Image, ImageTk
# Núcleo de comandos
from core.orchestrator import Orchestrator


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

orch = Orchestrator()

class LynxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lynx")
        self.geometry("360x200")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0f1113")

        # ---------------------------
        # Header com ícone e título
        # ---------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(10, 4))

        # círculo simbólico (ícone)
        self.icon_canvas = ctk.CTkCanvas(header, width=14, height=14, bg="#0f1113", highlightthickness=0)
        self.icon_canvas.create_oval(2, 2, 12, 12, fill="#2db7ff", outline="")
        self.icon_canvas.pack(side="left", padx=(0, 6))

        # título com glow
        self.label_title = ctk.CTkLabel(
            header,
            text="Lynx",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#21e066"
        )
        self.label_title.pack(side="left")

        # ---------------------------
        # Entrada
        # ---------------------------
        self.input = ctk.CTkEntry(
            self,
            placeholder_text="Digite o comando (ex: 'ln teste', 'vscode')",
            width=320,
            height=36,
            border_width=2,
            corner_radius=8
        )
        self.input.pack(pady=(10, 8))
        self.input.bind("<Return>", self.on_enter)

        # ---------------------------
        # Resultado
        # ---------------------------
        self.result = ctk.CTkLabel(
            self,
            text="",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=13)
        )
        self.result.pack(pady=(4, 10))

        # ---------------------------
        # Botões
        # ---------------------------
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 8))

        self.btn_close = ctk.CTkButton(btn_frame, text="Fechar", width=80, command=self.hide_window)
        self.btn_close.grid(row=0, column=0, padx=6)
        self.btn_help = ctk.CTkButton(btn_frame, text="ⓘ Ajuda", width=80, command=self.show_help)
        self.btn_help.grid(row=0, column=1, padx=6)
        self.btn_add = ctk.CTkButton(btn_frame, text="➕Adicionar Comando", width=80, command=self.show_add_command)
        self.btn_add.grid(row=0, column=2, padx=6)

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        # animação do ícone
        self.animate_icon()

    # ---------------------------
    # Animação: ícone pulsante
    # ---------------------------
    def animate_icon(self):
        import math, time
        t = time.time() * 2.5
        brightness = 0.6 + 0.4 * math.sin(t)
        color = f'#{int(40 * brightness):02x}{int(200 * brightness):02x}{int(90 * brightness):02x}'
        self.icon_canvas.delete("all")
        self.icon_canvas.create_oval(2, 2, 12, 12, fill=color, outline="")
        self.after(100, self.animate_icon)

    # ---------------------------
    # Evento Enter
    # ---------------------------
    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        response = orch.handle_input(cmd)
        result = response  # porque o Orchestrator já retorna texto direto
        self.show_result_feedback(result)
        self.input.delete(0, "end")

    # ---------------------------
    # Feedback visual
    # ---------------------------
    def show_result_feedback(self, text):
        self.result.configure(text=text, text_color="#29c85a")
        self.after(100, lambda: self.result.configure(text_color="#d0d0d0"))

    # ---------------------------
    # Outros métodos
    # ---------------------------
    def hide_window(self):
        self.quit()
        os._exit(0)


    def show_help(self):
        

        # ---------------------------
        # Janela principal
        # ---------------------------
        h = ctk.CTkToplevel(self)
        h.title("Lynx — Ajuda e Comandos")
        h.geometry("650x540")
        h.attributes("-topmost", True)
        h.configure(fg_color="#101214")


        # ---------------------------
        # Barra de busca
        # ---------------------------
        search_frame = ctk.CTkFrame(h, fg_color="#15171a", corner_radius=10)
        search_frame.pack(fill="x", padx=12, pady=(12, 6))


        search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Buscar comando, alias ou descrição...",
        height=36,
        corner_radius=10
        )
        search_entry.pack(fill="x", padx=12, pady=12)


        # ---------------------------
        # Área scrollável
        # ---------------------------
        scroll_frame = ctk.CTkScrollableFrame(h, fg_color="#15171a", corner_radius=12)
        scroll_frame.pack(fill="both", expand=True, padx=12, pady=6)


        # ---------------------------
        # Transformar os comandos do engine para exibição
        # ---------------------------
        command_cards = []

        for cmd in orch.engine.commands:
            main_cmd = cmd["keywords"][0]
            aliases = ", ".join(cmd["keywords"][1:]) if len(cmd["keywords"]) > 1 else "—"

            ctype = cmd.get("type", "")

            if ctype in ("url", "external"):
                action = "Abre um site"
            elif ctype == "executable":
                action = "Executa um programa"
            elif ctype == "system":
                action = "Ação do sistema"
            else:
                action = "—"

            card = ctk.CTkFrame(scroll_frame, fg_color="#1b1e21", corner_radius=10)
            card.pack(fill="x", padx=8, pady=6)

            lbl_cmd = ctk.CTkLabel(
                card,
                text=main_cmd,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#00b4ff"
            )
            lbl_cmd.pack(anchor="w", padx=12, pady=(10, 2))

            lbl_alias = ctk.CTkLabel(
                card,
                text=f"Aliases: {aliases}",
                font=ctk.CTkFont(size=12),
                text_color="#a8b3bd"
            )
            lbl_alias.pack(anchor="w", padx=12)

            lbl_action = ctk.CTkLabel(
                card,
                text=f"Ação: {action}",
                font=ctk.CTkFont(size=12),
                text_color="#d0d0d0"
            )
            lbl_action.pack(anchor="w", padx=12, pady=(0, 10))

            command_cards.append((card, main_cmd, aliases, action))



        # ---------------------------
        # Função de filtro
        # ---------------------------
        def apply_filter(event=None):
            text = search_entry.get().lower().strip()
            for card, cmd, alias, action in command_cards:
                data = f"{cmd} {alias} {action}".lower()
                card.pack_forget()
                if text in data:
                    card.pack(fill="x", padx=8, pady=6)


        search_entry.bind("<KeyRelease>", apply_filter)



    def show_add_command(self):

        # ---------------------------
        # Helpers
        # ---------------------------
        def is_url(s: str):
            try:
                p = urlparse(s)
                return p.scheme in ("http", "https") and p.netloc != ""
            except Exception:
                return False

        def file_exists(s: str):
            return os.path.exists(s) and os.path.isfile(s)

        def guess_type(s: str):
            if is_url(s):
                return "external"
            if file_exists(s):
                return "internal"
            return None

        def load_json():
            if not os.path.exists("data/commands.json"):
                with open("data/commands.json", "w", encoding="utf-8") as f:
                    json.dump({"commands": [], "recent": []}, f, indent=4, ensure_ascii=False)

            with open("data/commands.json", "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"commands": [], "recent": []}

        def save_json(data):
            with open("commands.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        def add_recent(name):
            data = load_json()
            rec = data.get("recent", [])
            if name in rec:
                rec.remove(name)
            rec.insert(0, name)
            data["recent"] = rec[:6]
            save_json(data)

        # ---------------------------
        # Window
        # ---------------------------
        win = ctk.CTkToplevel(self)
        win.title("Adicionar Comando — Lynx")
        win.geometry("650x520")
        win.attributes("-topmost", True)
        win.configure(fg_color="#0f1113")
        win.selected_icon = None

        # ---------------------------
        # Header
        # ---------------------------
        lbl = ctk.CTkLabel(
            win,
            text="Adicionar novo comando",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#21e066"
        )
        lbl.pack(pady=(12, 4))

        # ---------------------------
        # Main frame (tela única)
        # ---------------------------
        main = ctk.CTkFrame(win, fg_color="#101214", corner_radius=10)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        # ---- Nome ----
        lbl_name = ctk.CTkLabel(main, text="Nome do comando", anchor="w")
        lbl_name.pack(fill="x", padx=12, pady=(12, 4))
        entry_name = ctk.CTkEntry(main)
        entry_name.pack(fill="x", padx=12)

        # ---- Keywords ----
        lbl_keywords = ctk.CTkLabel(main, text="Palavras-chave (Enter para adicionar)", anchor="w")
        lbl_keywords.pack(fill="x", padx=12, pady=(12, 4))

        keyword_var = tk.StringVar()
        entry_kw = ctk.CTkEntry(main, textvariable=keyword_var)
        entry_kw.pack(fill="x", padx=12)

        chips_frame = ctk.CTkFrame(main, fg_color="transparent")
        chips_frame.pack(fill="x", padx=12, pady=(6, 10))

        chips = []

        def redraw_chips():
            for w in chips_frame.winfo_children():
                w.destroy()

            for k in chips:
                wrap = Frame(chips_frame, bg="#101217")
                wrap.pack(side="left", padx=6, pady=6)
                Label(wrap, text=k, fg="#cbd5db", bg="#101217", padx=8, pady=4).pack(side="left")
                ctk.CTkButton(
                    wrap,
                    text="x",
                    width=26,
                    height=22,
                    corner_radius=8,
                    command=lambda key=k: remove_chip(key)
                ).pack(side="left", padx=(6,0))

        def add_chip(event=None):
            v = entry_kw.get().strip().lower()
            if not v:
                return

            parts = [p.strip() for p in v.replace(";",",").split(",") if p.strip()]
            changed = False

            for p in parts:
                if p not in chips:
                    chips.append(p)
                    changed = True

            if changed:
                redraw_chips()

            entry_kw.delete(0, "end")

        def remove_chip(key):
            if key in chips:
                chips.remove(key)
                redraw_chips()

        entry_kw.bind("<Return>", add_chip)

        # ---- Caminho/URL ----
        lbl_path = ctk.CTkLabel(main, text="Caminho ou URL", anchor="w")
        lbl_path.pack(fill="x", padx=12, pady=(4, 4))

        entry_path = ctk.CTkEntry(main)
        entry_path.pack(fill="x", padx=12)

        # ---- Botões de arquivo e ícone ----
        row = ctk.CTkFrame(main, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(10, 10))

        def pick_file():
            p = filedialog.askopenfilename(title="Selecione o executável")
            if p:
                entry_path.delete(0, "end")
                entry_path.insert(0, p)
                detect_type()

        def pick_icon():
            p = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.ico;*.jpg;*.jpeg")])
            if p:
                win.selected_icon = p
                load_icon_preview(p)

        ctk.CTkButton(row, text="Escolher arquivo", width=150, command=pick_file).pack(side="left")
        ctk.CTkButton(row, text="Selecionar ícone", width=150, command=pick_icon).pack(side="left", padx=(10,0))

        # ---- Preview + type hint ----
        type_hint = ctk.CTkLabel(main, text="Tipo: —", anchor="w", text_color="#a0a9ad")
        type_hint.pack(fill="x", padx=12)

        preview = ctk.CTkLabel(main, text="Preview:", anchor="w", justify="left")
        preview.pack(fill="x", padx=12, pady=(6, 10))

        icon_preview_frame = ctk.CTkFrame(main, fg_color="transparent")
        icon_preview_frame.pack(fill="x", padx=12)
        icon_label = ctk.CTkLabel(icon_preview_frame, text="Ícone: (nenhum)", anchor="w")
        icon_label.pack(side="left")
        icon_holder = ctk.CTkFrame(icon_preview_frame, fg_color="transparent")
        icon_holder.pack(side="right")

        def load_icon_preview(path):
            for w in icon_holder.winfo_children():
                w.destroy()
            try:
                img = Image.open(path)
                img.thumbnail((48,48))
                tkimg = ImageTk.PhotoImage(img)
                lbl = ctk.CTkLabel(icon_holder, image=tkimg, text="")
                lbl.image = tkimg
                lbl.pack()
                icon_label.configure(text=f"Ícone: {os.path.basename(path)}")
            except:
                icon_label.configure(text="Ícone: (erro)")

        # ---- Detectar tipo ----
        def detect_type(event=None):
            p = entry_path.get().strip()
            t = guess_type(p)

            if t == "external":
                type_hint.configure(text="Tipo: URL", text_color="#7bd389")
            elif t == "internal":
                type_hint.configure(text="Tipo: Programa", text_color="#7bd389")
            else:
                type_hint.configure(text="Tipo: inválido", text_color="#ff8080")

            update_preview()

        entry_path.bind("<FocusOut>", detect_type)
        entry_path.bind("<KeyRelease>", lambda e: update_preview())

        # ---- Preview ----
        def update_preview():
            n = entry_name.get().strip() or "(não definido)"
            ks = ", ".join(chips) if chips else "(nenhuma)"
            target = entry_path.get().strip()
            target_type = "URL" if is_url(target) else "Arquivo" if file_exists(target) else "(inválido)"

            preview.configure(text=f"Preview:\n- Nome: {n}\n- Keywords: {ks}\n- Target: {target_type}")

        entry_name.bind("<KeyRelease>", lambda e: update_preview())

        # ---- Recentes ----
        recent_label = ctk.CTkLabel(main, text="Recentes:", anchor="w", text_color="#a8b3bd")
        recent_label.pack(fill="x", padx=12, pady=(6, 2))

        recent_frame = ctk.CTkFrame(main, fg_color="transparent")
        recent_frame.pack(fill="x", padx=12, pady=(0,12))

        def load_recent():
            data = load_json()
            for w in recent_frame.winfo_children():
                w.destroy()

            for name in data.get("recent", []):
                btn = ctk.CTkButton(
                    recent_frame, 
                    text=name, 
                    width=120,
                    command=lambda n=name: fill_recent(n)
                )
                btn.pack(side="left", padx=6)

        def fill_recent(name):
            data = load_json()
            for c in data.get("commands", []):
                if c.get("name") == name:
                    entry_name.delete(0,"end")
                    entry_name.insert(0, name)

                    chips.clear()
                    chips.extend(c.get("keywords", []))
                    redraw_chips()

                    if c["type"] == "internal":
                        entry_path.delete(0,"end")
                        entry_path.insert(0, c.get("path",""))
                    else:
                        entry_path.delete(0,"end")
                        entry_path.insert(0, c.get("url",""))

                    detect_type()
                    break

        load_recent()
        update_preview()

        # ---------------------------
        # Rodapé: Testar / Salvar
        # ---------------------------
        footer = ctk.CTkFrame(win, fg_color="transparent")
        footer.pack(fill="x", padx=12, pady=12)

        status = ctk.CTkLabel(footer, text="", anchor="w", text_color="#a8b3bd")
        status.pack(side="left")

        def set_status(msg, ok=True):
            status.configure(text=msg, text_color="#7bd389" if ok else "#ff7373")
            win.after(2500, lambda: status.configure(text=""))

        # ---- Testar ----
        def test_cmd():
            tgt = entry_path.get().strip()
            if is_url(tgt):
                webbrowser.open(tgt)
                set_status("URL aberta.")
            elif file_exists(tgt):
                subprocess.Popen(tgt, shell=True)
                set_status("Programa iniciado.")
            else:
                set_status("Destino inválido.", ok=False)

        ctk.CTkButton(footer, text="Testar", width=120, command=test_cmd).pack(side="right", padx=(6,0))

        # ---- Salvar ----
        def save():
            name = entry_name.get().strip()
            if not name:
                return set_status("Nome obrigatório.", ok=False)

            data = load_json()
            if any(c.get("name")==name for c in data["commands"]):
                return set_status("Nome já existe.", ok=False)

            if not chips:
                return set_status("Adicione keywords.", ok=False)

            target = entry_path.get().strip()
            if not target or not (is_url(target) or file_exists(target)):
                return set_status("Destino inválido.", ok=False)

            t = "external" if is_url(target) else "internal"
            cmd_data = {
                "name": name,
                "keywords": chips.copy(),
                "type": t
            }

            if t == "external":
                cmd_data["url"] = target
            else:
                cmd_data["path"] = target

            if win.selected_icon:
                cmd_data["icon"] = win.selected_icon

            data["commands"].append(cmd_data)
            save_json(data)
            add_recent(name)
            load_recent()

            # Runtime
            if t == "internal":
                engine.commands[tuple(chips.copy())] = lambda p=target: subprocess.Popen(p, shell=True)
            else:
                engine.commands[tuple(chips.copy())] = lambda u=target: webbrowser.open(u)

            set_status("Comando salvo com sucesso!")
            win.after(700, win.destroy)

        ctk.CTkButton(footer, text="Salvar", width=120, command=save).pack(side="right")

    # ---------------------------
    # Tray Icon
    # ---------------------------
def create_tray(app):
    def on_show(icon, item):
        app.deiconify()

    def on_quit(icon, item):
        try:
            icon.stop()  # para o tray loop
            app.quit()   # encerra o mainloop do Tkinter
            os._exit(0)  # força término completo do processo
        except Exception:
            os._exit(0)

    image = Image.new("RGB", (64, 64), (0, 153, 255))
    menu = Menu(
        MenuItem("Mostrar Lynx", on_show),
        MenuItem("Sair", on_quit)
    )
    icon = Icon("Lynx", image, "Lynx Assistant", menu)
    icon.run()


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app = LynxApp()
    tray_thread = threading.Thread(target=create_tray, args=(app,), daemon=True)
    tray_thread.start()
    app.mainloop()
