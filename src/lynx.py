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
import customtkinter as ctk
import os
import json
import subprocess
import webbrowser
import threading
from urllib.parse import urlparse

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageTk
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
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(10, 4))
        self.icon_canvas = ctk.CTkCanvas(header, width=14, height=14, bg="#0f1113", highlightthickness=0)
        self.icon_canvas.create_oval(2, 2, 12, 12, fill="#2db7ff", outline="")
        self.icon_canvas.pack(side="left", padx=(0, 6))
        self.label_title = ctk.CTkLabel(
            header,
            text="Lynx",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#21e066"
        )
        self.label_title.pack(side="left")
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
        self.result = ctk.CTkLabel(
            self,
            text="",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=13)
        )
        self.result.pack(pady=(4, 10))
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 8))
        self.btn_close = ctk.CTkButton(btn_frame, text="Fechar", width=80, command=self.hide_window)
        self.btn_close.grid(row=0, column=0, padx=6)
        self.btn_help = ctk.CTkButton(btn_frame, text="ⓘ Ajuda", width=80, command=self.show_help)
        self.btn_help.grid(row=0, column=1, padx=6)
        self.btn_add = ctk.CTkButton(btn_frame, text="➕Adicionar Comando", width=80, command=self.show_add_command)
        self.btn_add.grid(row=0, column=2, padx=6)
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.animate_icon()
    def animate_icon(self):
        import math, time
        t = time.time() * 2.5
        brightness = 0.6 + 0.4 * math.sin(t)
        color = f'#{int(40 * brightness):02x}{int(200 * brightness):02x}{int(90 * brightness):02x}'
        self.icon_canvas.delete("all")
        self.icon_canvas.create_oval(2, 2, 12, 12, fill=color, outline="")
        self.after(100, self.animate_icon)
    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        response = orch.handle_input(cmd)
        result = response  # porque o Orchestrator já retorna texto direto
        self.show_result_feedback(result)
        self.input.delete(0, "end")

    def show_result_feedback(self, text):
        self.result.configure(text=text, text_color="#29c85a")
        self.after(100, lambda: self.result.configure(text_color="#d0d0d0"))

    def hide_window(self):
        self.quit()
        os._exit(0)


    def show_help(self):
        
        h = ctk.CTkToplevel(self)
        h.title("Lynx — Ajuda e Comandos")
        h.geometry("650x540")
        h.attributes("-topmost", True)
        h.configure(fg_color="#101214")
        search_frame = ctk.CTkFrame(h, fg_color="#15171a", corner_radius=10)
        search_frame.pack(fill="x", padx=12, pady=(12, 6))


        search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Buscar comando, alias ou descrição...",
        height=36,
        corner_radius=10
        )
        search_entry.pack(fill="x", padx=12, pady=12)
        scroll_frame = ctk.CTkScrollableFrame(h, fg_color="#15171a", corner_radius=12)
        scroll_frame.pack(fill="both", expand=True, padx=12, pady=6)
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

        def apply_filter(event=None):
            text = search_entry.get().lower().strip()
            for card, cmd, alias, action in command_cards:
                data = f"{cmd} {alias} {action}".lower()
                card.pack_forget()
                if text in data:
                    card.pack(fill="x", padx=8, pady=6)
        search_entry.bind("<KeyRelease>", apply_filter)
    
    def show_add_command(self):
        def is_url(s: str):
            from urllib.parse import urlparse
            try:
                p = urlparse(s)
                return p.scheme in ("http", "https") and p.netloc != ""
            except:
                return False

        def file_exists(s: str):
            return os.path.exists(s) and os.path.isfile(s)

        def load_json():
            if not os.path.exists("data/commands.json"):
                with open("data/commands.json", "w", encoding="utf-8") as f:
                    json.dump({"commands": [], "recent": []}, f, indent=4)
            with open("data/commands.json", "r", encoding="utf-8") as f:
                return json.load(f)

        def save_json(data):
            with open("data/commands.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)


        win = ctk.CTkToplevel(self)
        win.title("Adicionar Comando — Simples")
        win.geometry("440x380")
        win.attributes("-topmost", True)
        win.configure(fg_color="#0f1113")

        lbl_title = ctk.CTkLabel(
            win,
            text="Novo comando",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2ee680"
        )
        lbl_title.pack(pady=(12, 8))

        ctk.CTkLabel(win, text="Nome:", anchor="w").pack(fill="x", padx=12)
        entry_name = ctk.CTkEntry(win)
        entry_name.pack(fill="x", padx=12, pady=6)
        ctk.CTkLabel(win, text="Keywords (separadas por vírgula):", anchor="w").pack(fill="x", padx=12)
        entry_keywords = ctk.CTkEntry(win)
        entry_keywords.pack(fill="x", padx=12, pady=6)
        ctk.CTkLabel(win, text="Caminho ou URL:", anchor="w").pack(fill="x", padx=12)
        entry_target = ctk.CTkEntry(win)
        entry_target.pack(fill="x", padx=12, pady=6)
        def pick_file():
            p = filedialog.askopenfilename(title="Selecionar arquivo")
            if p:
                entry_target.delete(0, "end")
                entry_target.insert(0, p)

        ctk.CTkButton(win, text="Escolher arquivo", command=pick_file).pack(pady=(0,12))
        win.selected_icon = None

        def pick_icon():
            p = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.ico;*.jpg")])
            if p:
                win.selected_icon = p
                lbl_icon.configure(text=f"Ícone selecionado: {os.path.basename(p)}")

        lbl_icon = ctk.CTkLabel(win, text="Nenhum ícone selecionado", text_color="#a8b3bd")
        lbl_icon.pack(pady=(0,4))

        ctk.CTkButton(win, text="Selecionar ícone (opcional)", command=pick_icon).pack(pady=(0,12))
        status = ctk.CTkLabel(win, text="", text_color="#a8b3bd")
        status.pack()

        def set_status(msg, ok=True):
            status.configure(text=msg, text_color=("#2ee680" if ok else "#ff7373"))
            win.after(2500, lambda: status.configure(text=""))

        def test_cmd():
            tgt = entry_target.get().strip()
            if is_url(tgt):
                webbrowser.open(tgt)
                set_status("URL aberta.")
            elif file_exists(tgt):
                subprocess.Popen(tgt, shell=True)
                set_status("Programa iniciado.")
            else:
                set_status("Destino inválido", ok=False)
                
        def save():
            name = entry_name.get().strip()
            if not name:
                return set_status("Nome obrigatório.", ok=False)

            keywords = [k.strip().lower() for k in entry_keywords.get().split(",") if k.strip()]
            if not keywords:
                return set_status("Adicione keywords.", ok=False)

            target = entry_target.get().strip()
            if not (is_url(target) or file_exists(target)):
                return set_status("Destino inválido.", ok=False)

            data = load_json()

            if any(c.get("name") == name for c in data["commands"]):
                return set_status("Nome já existe.", ok=False)

            cmd_data = {
                "name": name,
                "keywords": keywords,
                "type": "external" if is_url(target) else "internal",
                "url": target if is_url(target) else None,
                "path": target if file_exists(target) else None,
                "icon": win.selected_icon
            }

            data["commands"].append(cmd_data)
            save_json(data)

            set_status("Comando salvo!")
            win.after(500, win.destroy)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Testar", width=120, command=test_cmd).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="Salvar", width=120, command=save).grid(row=0, column=1, padx=6)

def create_tray(app):
    def on_show(icon, item):
        app.deiconify()

    def on_quit(icon, item):
        try:
            icon.stop()  
            app.quit()   
            os._exit(0)  
        except Exception:
            os._exit(0)

    image = Image.new("RGB", (64, 64), (0, 153, 255))
    menu = Menu(
        MenuItem("Mostrar Lynx", on_show),
        MenuItem("Sair", on_quit)
    )
    icon = Icon("Lynx", image, "Lynx Assistant", menu)
    icon.run()

if __name__ == "__main__":
    app = LynxApp()
    tray_thread = threading.Thread(target=create_tray, args=(app,), daemon=True)
    tray_thread.start()
    app.mainloop()
