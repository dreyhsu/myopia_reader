#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

class MyopiaReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Myopia Reader - Display Engine")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Text content
        self.current_text = ""
        self.current_file = None
        
        # Font settings
        self.font_size = 18
        self.font_family = "Arial"
        
        # Pagination settings
        self.lines_per_page = 30
        self.current_page = 1
        self.total_pages = 1
        self.text_lines = []
        
        # Setup UI
        self.setup_ui()
        
        # Auto-load from output folder if available
        self.auto_load_text_file()
    
    def setup_ui(self):
        # Menu bar
        menubar = tk.Menu(self.root, bg='#2d2d2d', fg='#ffffff')
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='#ffffff')
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Text File", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Control frame
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Font size controls
        tk.Label(control_frame, text="Font Size:", bg='#1a1a1a', fg='#ffffff', font=('Arial', 12)).pack(side='left', padx=5)
        
        font_size_var = tk.IntVar(value=self.font_size)
        font_size_scale = tk.Scale(control_frame, from_=12, to=56, orient='horizontal', 
                                 variable=font_size_var, command=self.update_font_size,
                                 bg='#2d2d2d', fg='#ffffff', highlightbackground='#1a1a1a')
        font_size_scale.pack(side='left', padx=10)
        
        # Page navigation controls
        page_frame = tk.Frame(control_frame, bg='#1a1a1a')
        page_frame.pack(side='left', padx=20)
        
        tk.Label(page_frame, text="Page:", bg='#1a1a1a', fg='#ffffff', font=('Arial', 12)).pack(side='left')
        
        # Previous page button
        self.prev_btn = tk.Button(page_frame, text="◀", command=self.prev_page,
                                 bg='#2d2d2d', fg='#ffffff', font=('Arial', 12),
                                 relief='flat', padx=8, pady=2)
        self.prev_btn.pack(side='left', padx=2)
        
        # Page entry
        self.page_var = tk.StringVar()
        self.page_entry = tk.Entry(page_frame, textvariable=self.page_var, width=5,
                                  bg='#2d2d2d', fg='#ffffff', font=('Arial', 12),
                                  justify='center', relief='flat')
        self.page_entry.pack(side='left', padx=2)
        self.page_entry.bind('<Return>', self.jump_to_page)
        
        # Page info label
        self.page_info_label = tk.Label(page_frame, text="of 1", bg='#1a1a1a', fg='#cccccc', font=('Arial', 12))
        self.page_info_label.pack(side='left', padx=2)
        
        # Next page button
        self.next_btn = tk.Button(page_frame, text="▶", command=self.next_page,
                                 bg='#2d2d2d', fg='#ffffff', font=('Arial', 12),
                                 relief='flat', padx=8, pady=2)
        self.next_btn.pack(side='left', padx=2)
        
        # Jump to page button
        jump_btn = tk.Button(page_frame, text="Go", command=self.jump_to_page,
                           bg='#404040', fg='#ffffff', font=('Arial', 10),
                           relief='flat', padx=8, pady=2)
        jump_btn.pack(side='left', padx=5)
        
        # File info label
        self.file_info_label = tk.Label(control_frame, text="No file loaded", 
                                       bg='#1a1a1a', fg='#cccccc', font=('Arial', 10))
        self.file_info_label.pack(side='right', padx=10)
        
        # Main text area with scrollbar
        text_frame = tk.Frame(self.root, bg='#1a1a1a')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, bg='#2d2d2d')
        scrollbar.pack(side='right', fill='y')
        
        # Text widget with dark theme
        self.text_widget = tk.Text(text_frame, 
                                  bg='#1a1a1a',           # Dark background
                                  fg='#e0e0e0',           # Light text
                                  insertbackground='#ffffff',  # White cursor
                                  selectbackground='#404040',  # Selection color
                                  selectforeground='#ffffff',  # Selected text color
                                  font=(self.font_family, self.font_size),
                                  wrap='word',
                                  yscrollcommand=scrollbar.set,
                                  relief='flat',
                                  borderwidth=0,
                                  padx=20,
                                  pady=20,
                                  spacing1=5,   # Space before paragraphs
                                  spacing2=3,   # Space between lines
                                  spacing3=5    # Space after paragraphs
                                  )
        self.text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.text_widget.yview)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief='sunken', anchor='w',
                                  bg='#2d2d2d', fg='#ffffff', font=('Arial', 9))
        self.status_bar.pack(side='bottom', fill='x')
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-plus>', lambda e: self.increase_font_size())
        self.root.bind('<Control-minus>', lambda e: self.decrease_font_size())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Left>', lambda e: self.prev_page())
        self.root.bind('<Right>', lambda e: self.next_page())
        self.root.bind('<Prior>', lambda e: self.prev_page())  # Page Up
        self.root.bind('<Next>', lambda e: self.next_page())   # Page Down
        
    def auto_load_text_file(self):
        """Automatically load a text file from the output folder if it exists"""
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        
        if os.path.exists(output_folder):
            # Look for .txt files in the output folder
            txt_files = [f for f in os.listdir(output_folder) if f.endswith('.txt')]
            if txt_files:
                # Load the first text file found
                file_path = os.path.join(output_folder, txt_files[0])
                self.load_text_file(file_path)
                return
        
        # If no output folder or txt files, show instructions
        self.text_widget.insert('1.0', """Welcome to Myopia Reader - Display Engine

This application displays text files with a dark theme and large fonts optimized for reading with myopia.

Features:
• Dark background with high-contrast light text
• Adjustable font size (12-56pt)
• Page navigation with jump-to-page functionality
• Word wrapping for comfortable reading
• Smooth scrolling

To get started:
1. Place a .txt file in the 'output' folder, or
2. Use File → Open Text File to select any text file
3. Adjust font size using the slider or Ctrl+/Ctrl- shortcuts

Keyboard Shortcuts:
• Ctrl+O: Open file
• Ctrl+Plus: Increase font size
• Ctrl+Minus: Decrease font size
• Ctrl+Q: Quit application
• Arrow Keys/Page Up/Down: Navigate pages
• Enter in page box: Jump to specific page

The application will automatically load text files from the 'output' folder when started.
""")
        self.status_bar.config(text="No text file found in output folder - use File → Open to select a file")
        
    def open_file(self):
        """Open file dialog to select a text file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        )
        
        if file_path:
            self.load_text_file(file_path)
    
    def load_text_file(self, file_path):
        """Load and display text from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update content
            self.current_file = file_path
            self.current_text = content
            
            # Split text into lines for pagination
            self.text_lines = content.split('\n')
            self.calculate_pagination()
            
            # Display first page
            self.current_page = 1
            self.display_current_page()
            
            # Update UI
            file_name = os.path.basename(file_path)
            self.file_info_label.config(text=f"File: {file_name}")
            self.status_bar.config(text=f"Loaded: {file_path} ({len(content):,} characters, {self.total_pages} pages)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_bar.config(text=f"Error loading file: {str(e)}")
    
    def calculate_pagination(self):
        """Calculate total pages based on lines per page"""
        if not self.text_lines:
            self.total_pages = 1
            return
        
        # Calculate lines per page based on text widget height and font size
        # This is an approximation - adjust based on testing
        widget_height = self.text_widget.winfo_height()
        if widget_height > 1:
            # Estimate lines that fit in the visible area
            line_height = self.font_size + 8  # Font size + spacing
            visible_lines = max(1, (widget_height - 40) // line_height)  # 40px for padding
            self.lines_per_page = max(10, visible_lines - 2)  # Minimum 10 lines, leave some buffer
        
        self.total_pages = max(1, (len(self.text_lines) + self.lines_per_page - 1) // self.lines_per_page)
    
    def display_current_page(self):
        """Display the current page of text"""
        if not self.text_lines:
            return
        
        # Calculate start and end line indices
        start_line = (self.current_page - 1) * self.lines_per_page
        end_line = min(start_line + self.lines_per_page, len(self.text_lines))
        
        # Get page content
        page_lines = self.text_lines[start_line:end_line]
        page_content = '\n'.join(page_lines)
        
        # Update text widget
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', page_content)
        
        # Update page info
        self.page_var.set(str(self.current_page))
        self.page_info_label.config(text=f"of {self.total_pages}")
        
        # Update button states
        self.prev_btn.config(state='normal' if self.current_page > 1 else 'disabled')
        self.next_btn.config(state='normal' if self.current_page < self.total_pages else 'disabled')
        
        # Move cursor to beginning
        self.text_widget.mark_set('insert', '1.0')
        self.text_widget.see('1.0')
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_current_page()
    
    def jump_to_page(self, event=None):
        """Jump to specific page number"""
        try:
            target_page = int(self.page_var.get())
            if 1 <= target_page <= self.total_pages:
                self.current_page = target_page
                self.display_current_page()
            else:
                messagebox.showwarning("Invalid Page", f"Page number must be between 1 and {self.total_pages}")
                self.page_var.set(str(self.current_page))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid page number")
            self.page_var.set(str(self.current_page))
    
    def update_font_size(self, value):
        """Update font size from scale widget"""
        self.font_size = int(value)
        self.text_widget.config(font=(self.font_family, self.font_size))
        
        # Recalculate pagination when font size changes
        if self.text_lines:
            self.calculate_pagination()
            # Adjust current page if it's now out of bounds
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
            self.display_current_page()
        
    def increase_font_size(self):
        """Increase font size"""
        if self.font_size < 56:
            self.font_size += 2
            self.text_widget.config(font=(self.font_family, self.font_size))
            if self.text_lines:
                self.calculate_pagination()
                if self.current_page > self.total_pages:
                    self.current_page = self.total_pages
                self.display_current_page()
    
    def decrease_font_size(self):
        """Decrease font size"""
        if self.font_size > 12:
            self.font_size -= 2
            self.text_widget.config(font=(self.font_family, self.font_size))
            if self.text_lines:
                self.calculate_pagination()
                if self.current_page > self.total_pages:
                    self.current_page = self.total_pages
                self.display_current_page()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = MyopiaReader()
    app.run()

if __name__ == "__main__":
    main()