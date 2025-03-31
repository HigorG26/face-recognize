import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import cv2
import numpy as np
import shutil

class InterfaceGrafica:
    def __init__(self, root, processador):
        self.root = root
        self.root.title("Processador de Imagens e Detector de Rostos")
        self.processador = processador
        self.arquivos_selecionados = []
        self.criar_interface()
        
    def criar_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10)
        
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.grid(row=0, column=1, padx=10)
        self.preview_frame = ttk.Frame(self.right_frame)
        self.preview_frame.grid(row=0, column=0, pady=5)
        self.results_frame = ttk.Frame(self.right_frame)
        self.results_frame.grid(row=1, column=0, pady=5)
        self.results_label = ttk.Label(self.results_frame, 
                                     text="Imagens com Rostos Detectados")
        self.results_label.grid(row=0, column=0, pady=5)
        self.canvas = tk.Canvas(self.results_frame, width=500, height=300)
        self.scrollbar_y = ttk.Scrollbar(self.results_frame, 
                                        orient="vertical", 
                                        command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.results_frame, 
                                        orient="horizontal", 
                                        command=self.canvas.xview)
        self.images_frame = ttk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set,
                             xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.scrollbar_x.grid(row=2, column=0, sticky="ew")
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.create_window((0, 0), window=self.images_frame, anchor="nw")
        self.images_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.frame_width)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        ttk.Button(left_frame, text="Selecionar Imagens", 
                   command=self.selecionar_arquivos).grid(row=0, column=0, pady=10)
        self.lista_arquivos = tk.Listbox(left_frame, width=30, height=20)
        self.lista_arquivos.grid(row=1, column=0, pady=10)
        self.lista_arquivos.bind('<<ListboxSelect>>', self.mostrar_preview)
        self.progresso = ttk.Progressbar(left_frame, orient="horizontal", 
                                       length=300, mode="determinate")
        self.progresso.grid(row=2, column=0, pady=10)
        self.status_label = ttk.Label(left_frame, text="")
        self.status_label.grid(row=3, column=0, pady=5)
        self.btn_processar = ttk.Button(left_frame, text="Processar Imagens", 
                                       command=self.processar_imagens, 
                                       state='disabled')
        self.btn_processar.grid(row=4, column=0, pady=10)
    
    def on_frame_configure(self, event=None):
        """Resetar a região de scroll do canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def frame_width(self, event):
        """Ajustar a largura do canvas"""
        canvas_width = event.width
        self.canvas.itemconfig(1, width=canvas_width)
    
    def _on_mousewheel(self, event):
        """Scroll com mouse wheel"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def mostrar_preview(self, event=None):
        if not self.lista_arquivos.curselection():
            return
            
        idx = self.lista_arquivos.curselection()[0]
        arquivo = self.arquivos_selecionados[idx]
        
        resultado = self.processador.processar_uma_imagem(arquivo)
        if resultado is None:
            return
        
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        fig = Figure(figsize=(10, 8))
        
        ax1 = fig.add_subplot(211)
        ax1.imshow(resultado['resultado'], cmap='gray')
        ax1.set_title(f"Processamento - {resultado['num_objetos']} objetos encontrados")
        ax1.axis('off')
        
        ax2 = fig.add_subplot(212)
        ax2.imshow(cv2.cvtColor(resultado['img_faces'], cv2.COLOR_BGR2RGB))
        ax2.set_title(f"{len(resultado['faces'])} face(s) encontrada(s)")
        ax2.axis('off')
        
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione as imagens",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            self.lista_arquivos.delete(0, tk.END)
            for arquivo in self.arquivos_selecionados:
                self.lista_arquivos.insert(tk.END, os.path.basename(arquivo))
            self.btn_processar['state'] = 'normal'
            self.status_label['text'] = f"{len(arquivos)} imagens selecionadas"
    
    def criar_diretorios(self):
        diretorios = ['imagens_com_rosto', 'imagens_sem_rosto']
        for dir in diretorios:
            if not os.path.exists(dir):
                os.makedirs(dir)
        return diretorios
    
    def mostrar_imagens_detectadas(self, imagens_com_rosto):
        """Mostra as imagens com rostos detectados em um grid"""
        for widget in self.images_frame.winfo_children():
            widget.destroy()
        
        thumb_size = (100, 100)
        max_por_linha = 4
        
        for idx, img_path in enumerate(imagens_com_rosto):
            try:
                img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 
                                 cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img)
                pil_img.thumbnail(thumb_size)
                
                photo = ImageTk.PhotoImage(pil_img)
                row = idx // max_por_linha
                col = idx % max_por_linha
                img_frame = ttk.Frame(self.images_frame)
                img_frame.grid(row=row, column=col, padx=5, pady=5)
                img_label = ttk.Label(img_frame, image=photo)
                img_label.image = photo
                img_label.pack()
                
                nome = os.path.basename(img_path)
                ttk.Label(img_frame, 
                         text=nome[:15] + '...' if len(nome) > 15 else nome,
                         wraplength=100).pack()
                
            except Exception as e:
                print(f"Erro ao mostrar miniatura: {str(e)}")
        self.on_frame_configure()
    
    def processar_imagens(self):
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada!")
            return
        
        dir_com_rosto, dir_sem_rosto = self.criar_diretorios()
        total = len(self.arquivos_selecionados)
        encontrados = 0
        nao_encontrados = 0
        imagens_com_rosto = []
        
        self.progresso['maximum'] = total
        self.btn_processar['state'] = 'disabled'
        
        for i, arquivo in enumerate(self.arquivos_selecionados, 1):
            self.status_label['text'] = f"Processando: {os.path.basename(arquivo)}"
            self.progresso['value'] = i
            self.root.update()
            
            try:
                resultado = self.processador.processar_uma_imagem(arquivo)
                if resultado is None:
                    continue
                    
                if resultado['tem_rosto']:
                    encontrados += 1
                    imagens_com_rosto.append(arquivo)
                    shutil.copy2(arquivo, os.path.join(dir_com_rosto, os.path.basename(arquivo)))
                else:
                    nao_encontrados += 1
                    shutil.copy2(arquivo, os.path.join(dir_sem_rosto, os.path.basename(arquivo)))
                    
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {str(e)}")
                continue
        
        self.mostrar_imagens_detectadas(imagens_com_rosto)
        self.status_label['text'] = f"Processamento concluído! {encontrados} com rosto, {nao_encontrados} sem rosto"
        self.btn_processar['state'] = 'normal'
