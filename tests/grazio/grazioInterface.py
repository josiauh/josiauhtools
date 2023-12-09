import gradio as gr
from josiauhtools_josiauh import grazio

def celsius_to_fahrenheit(celsius):
    if celsius < -273.15:
        return 0
    else:
        return celsius * 9/5+32

def intfFn(name, isMorning, celcius, news):
    greeting = "Good morning, everyone!" if isMorning else "Good evening, everyone!"
    return f"""
    {greeting} I'm your host, {name}. The weather is {celcius} degrees celcius, and now to the news.
    {news}
    """, celsius_to_fahrenheit(celcius)


intf = gr.Interface(
    fn=intfFn,
    inputs=["text", "checkbox", gr.Slider(-273.15, 100), "text"],
    outputs=["text", "number"],
    theme=grazio.Themes.RedVelvet
)

if __name__ == "__main__":
    intf.launch()