import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

imagem_path = ""
area_terreno = ""
imagem = None
imagem_final = None
pontos = []

def selecionar_imagem():
    global imagem_path
    caminho = filedialog.askopenfilename(
        title="Selecionar imagem do terreno",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
    )
    if caminho:
        imagem_path = caminho
        label_imagem.config(text=f"Imagem: {caminho.split('/')[-1]}")

def abrir_editor():
    global imagem, imagem_final, pontos, area_terreno

    if imagem_path == "":
        messagebox.showerror("Erro", "Selecione uma imagem.")
        return

    if entrada_area.get().strip() == "":
        messagebox.showerror("Erro", "Digite a área do terreno.")
        return

    area_terreno = entrada_area.get()

    imagem = cv2.imread(imagem_path)
    if imagem is None:
        messagebox.showerror("Erro", "Erro ao carregar imagem.")
        return

    imagem_final = imagem.copy()
    pontos = []

    cv2.imshow("Editor", imagem)
    cv2.setMouseCallback("Editor", clique)

def clique(event, x, y, flags, param):
    global pontos, imagem

    if event == cv2.EVENT_LBUTTONDOWN and len(pontos) < 4:
        pontos.append((x, y))

        cv2.circle(imagem, (x, y), 5, (0, 255, 255), -1)
        cv2.imshow("Editor", imagem)

        if len(pontos) == 4:
            desenhar_contorno()

def desenhar_contorno():
    global imagem_final

    pts = np.array(pontos, np.int32)
    pts = pts.reshape(-1, 1, 2)

    cv2.polylines(imagem_final, [pts], True, (0, 255, 255), 4)

    pts_array = np.array(pontos)
    centro_x = int(np.mean(pts_array[:, 0]))
    centro_y = int(np.mean(pts_array[:, 1]))

    texto = area_terreno

    (largura_texto, altura_texto), _ = cv2.getTextSize(
        texto,
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        3
    )

    pos_x = centro_x - largura_texto // 2
    pos_y = centro_y + altura_texto // 4

    imagem_pil = Image.fromarray(cv2.cvtColor(imagem_final, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(imagem_pil)

    fonte = ImageFont.truetype("arial.ttf", 30)

    texto = f"{area_terreno}m²"

    draw.text((pos_x, pos_y), texto, font=fonte, fill=(255, 255, 0))

    imagem_final = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)

    cv2.imshow("Editor", imagem_final)

def salvar_imagem():
    if imagem_final is None:
        messagebox.showerror("Erro", "Nenhuma imagem editada para salvar.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")]
    )

    if caminho:
        cv2.imwrite(caminho, imagem_final)
        messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")

janela = tk.Tk()
janela.title("Mapeador de Terrenos")
janela.geometry("800x500")
janela.resizable(False, False)

ttk.Label(janela, text="Mapeador de Terrenos",
          font=("Arial", 16, "bold")).pack(pady=10)

ttk.Button(janela, text="Selecionar Imagem",
           command=selecionar_imagem).pack(pady=5)

label_imagem = ttk.Label(janela, text="Nenhuma imagem selecionada")
label_imagem.pack()

ttk.Label(janela, text="Área do Terreno:",
          font=("Arial", 12)).pack(pady=10)

entrada_area = ttk.Entry(janela, font=("Arial", 12), justify="center")
entrada_area.pack()

ttk.Button(janela, text="Abrir Editor",
           command=abrir_editor).pack(pady=15)

ttk.Button(janela, text="Salvar Imagem Final",
           command=salvar_imagem).pack()

janela.mainloop()
