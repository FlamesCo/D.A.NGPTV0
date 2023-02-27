import tkinter
import requests

class ChatGPTClient(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
        }

        self.text_field = tkinter.Text(self)
        self.text_field.pack(side="top", fill="both", expand=True)
        self.text_field.config(state="disabled")

        self.entry_field = tkinter.Entry(self)
        self.entry_field.pack(side="bottom", fill="x")
        self.entry_field.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        message = self.entry_field.get()
        response = self.session.post("https://api.openai.com/v1/engines/chatgpt/jobs", headers=self.headers, json={
            "prompt": message,
            "max_tokens": 100,
            "temperature": 0.7,
        })
        if response.status_code == 200:
            response_json = response.json()
            self.text_field.config(state="normal")
            self.text_field.insert("end", f"You: {message}\n")
            self.text_field.insert("end", f"ChatGPT: {response_json['choices'][0]['text']}\n")
            self.text_field.config(state="normal")
        elif response.status_code == 401:
            # Unauthorized, prompt user for API key
            api_key = tkinter.simpledialog.askstring("API Key Required", "Please enter your API key for OpenAI:")
            if api_key:
                self.headers["Authorization"] = f"Bearer {api_key}"
                self.send_message()
            else:
                self.text_field.config(state="normal")
                self.text_field.insert("end", "Error: API key is required to use the OpenAI API.\n")
                self.text_field.config(state="normal")
        else:
            self.text_field.config(state="normal")
            self.text_field.insert("end", f"Error: Failed to get response from API (status code: {response.status_code})\n")
            self.text_field.config(state="normal")
        self.entry_field.delete(0, "end")

if __name__ == "__main__":
    app = ChatGPTClient()
    app.mainloop()
