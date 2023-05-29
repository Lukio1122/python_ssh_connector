import tkinter as tk
import paramiko

class SSHClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Client")

        self.ip_label = tk.Label(self.root, text="IP Address:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_ssh)
        self.connect_button.pack()

        self.terminal = tk.Text(self.root)
        self.terminal.pack()
        self.terminal.config(state=tk.DISABLED)

    def connect_ssh(self):
        ip = self.ip_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=username, password=password)

            self.terminal.config(state=tk.NORMAL)
            self.terminal.insert(tk.END, f"Connected to {ip}\n")
            self.terminal.config(state=tk.DISABLED)

            self.interactive_shell(client)

            client.close()
        except paramiko.AuthenticationException:
            self.terminal.config(state=tk.NORMAL)
            self.terminal.insert(tk.END, "Authentication failed. Please check your credentials.\n")
            self.terminal.config(state=tk.DISABLED)
        except paramiko.SSHException as e:
            self.terminal.config(state=tk.NORMAL)
            self.terminal.insert(tk.END, f"SSH connection failed: {str(e)}\n")
            self.terminal.config(state=tk.DISABLED)
        except Exception as e:
            self.terminal.config(state=tk.NORMAL)
            self.terminal.insert(tk.END, f"An error occurred: {str(e)}\n")
            self.terminal.config(state=tk.DISABLED)

    def interactive_shell(self, client):
        shell = client.invoke_shell()
        while True:
            try:
                data = shell.recv(1024).decode()
                if not data:
                    break
                self.terminal.config(state=tk.NORMAL)
                self.terminal.insert(tk.END, data)
                self.terminal.config(state=tk.DISABLED)
            except:
                break

            try:
                line = self.terminal.get(tk.END + "-2l", tk.END + "-1l")
                shell.send(line + "\n")
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    SSHClientGUI(root)
    root.mainloop()
