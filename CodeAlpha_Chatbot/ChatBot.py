import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.columns import Columns
from rich import box
import sys

console = Console()

def display_welcome():
    """Display a welcome banner"""
    welcome_text = Text("🤖 WELCOME TO Jarvis BOT", style="bold blue")
    console.print(Panel(welcome_text, 
                       subtitle="Your Friendly AI Companion", 
                       border_style="cyan",
                       box=box.DOUBLE))
    
    # Display features
    features = [
        "[green]✓[/green] Colorful responses",
        "[green]✓[/green] Interactive chat",
        "[green]✓[/green] Multiple conversation topics",
        "[green]✓[/green] Beautiful formatting",
        "[green]✓[/green] Conversation history"
    ]
    
    console.print("\n[bold]Features:[/bold]")
    for feature in features:
        console.print(f"  {feature}")
    
    console.print("\n[yellow]Type 'help' anytime to see available commands[/yellow]\n")

def create_response_table():
    """Create a table showing available commands"""
    table = Table(title="Available Commands", box=box.ROUNDED, border_style="cyan")
    table.add_column("Command", style="magenta", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Example", style="yellow")
    
    commands = [
        ("hello/hi/hey", "Greet the chatbot", "'hello' or 'hi there'"),
        ("how are you", "Ask about chatbot's mood", "'how are you?'"),
        ("joke", "Hear a funny joke", "'tell me a joke'"),
        ("weather", "Get weather information", "'what's the weather?'"),
        ("time", "Check current time", "'what time is it?'"),
        ("quote", "Get an inspirational quote", "'give me a quote'"),
        ("help", "Show this help table", "'help'"),
        ("bye/exit", "End the conversation", "'bye' or 'exit'"),
        ("color", "Change chat color theme", "'change color'")
    ]
    
    for cmd, desc, example in commands:
        table.add_row(cmd, desc, example)
    
    return table

def display_chat_message(role, message, color="cyan"):
    """Display a chat message with style"""
    if role.lower() == "user":
        panel = Panel.fit(f"[bold white]{message}[/bold white]", 
                         title="[bold cyan]You[/bold cyan]", 
                         border_style="cyan",
                         box=box.ROUNDED)
    else:
        panel = Panel.fit(message, 
                         title=f"[bold {color}]Jarvis[/bold {color}]", 
                         border_style=color,
                         box=box.ROUNDED)
    console.print(panel)

def get_joke():
    """Return a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a fish with no eyes? Fsh!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a factory that makes okay products? A satisfactory!"
    ]
    return random.choice(jokes)

def get_quote():
    """Return an inspirational quote"""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Life is what happens to you while you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It is during our darkest moments that we must focus to see the light. - Aristotle",
        "Whoever is happy will make others happy too. - Anne Frank"
    ]
    return random.choice(quotes)

def get_weather():
    """Return a fictional weather report"""
    weather_types = ["sunny ☀️", "rainy 🌧️", "cloudy ☁️", "snowy ❄️", "windy 🌬️"]
    temps = ["72°F (22°C)", "65°F (18°C)", "80°F (27°C)", "55°F (13°C)", "68°F (20°C)"]
    locations = ["your area", "the city", "outside your window"]
    
    weather = random.choice(weather_types)
    temp = random.choice(temps)
    location = random.choice(locations)
    
    return f"The weather in {location} is {weather} with a temperature of {temp}. Perfect for chatting!"

def chatbot_with_rich():
    """Enhanced chatbot with Rich library formatting"""
    
    # Display welcome message
    console.clear()
    display_welcome()
    
    # Color themes for responses
    color_themes = ["cyan", "green", "magenta", "yellow", "blue"]
    current_color = "cyan"
    
    # Conversation history
    history = []
    
    # Available responses
    greetings = [
        "[bold]Hi there![/bold] Great to meet you! 👋",
        "[bold]Hello![/bold] I'm excited to chat with you!",
        "[bold]Hey![/bold] Welcome to our conversation! 😊"
    ]
    
    how_are_you_responses = [
        "[bold]I'm fantastic![/bold] Running on pure Python power! 🐍",
        "[bold]I'm doing great![/bold] Thanks for asking! How about you?",
        "[bold]I'm wonderful![/bold] Chatting with you makes my circuits happy! 💖"
    ]
    
    goodbyes = [
        "[bold]Goodbye![/bold] Hope to chat with you again soon! 👋",
        "[bold]Farewell![/bold] This was fun! Come back anytime!",
        "[bold]See you later![/bold] Don't be a stranger! 😊"
    ]
    
    console.print("[cyan]Chat session started...[/cyan]\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input with rich prompt
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
            
            # Add to history
            history.append(("You", user_input))
            
            # Exit conditions
            if user_input.lower() in ['bye', 'goodbye', 'exit', 'quit']:
                response = random.choice(goodbyes)
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", response))
                
                # Show conversation summary
                console.print("\n[bold yellow]Conversation Summary:[/bold yellow]")
                console.print(f"Total messages exchanged: {len(history)}")
                
                if Confirm.ask("\n[bold]View conversation history?[/bold]"):
                    console.print("\n[bold]Conversation History:[/bold]")
                    for i, (speaker, msg) in enumerate(history, 1):
                        prefix = "[cyan]You:[/cyan]" if speaker == "You" else f"[{current_color}]Jarvis:[/{current_color}]"
                        console.print(f"{i:2}. {prefix} {msg}")
                
                console.print("\n[bold green]🤖 Chatbot session ended. Thank you for chatting![/bold green]")
                break
            
            # Help command
            elif user_input.lower() == 'help':
                console.print(create_response_table())
                response = "[bold]Here are all the things I can help with![/bold] Try any of these commands! ✨"
                history.append(("Jarvis", "Displayed help table"))
            
            # Greetings
            elif any(word in user_input.lower() for word in ['hello', 'hi', 'hey', 'greetings']):
                response = random.choice(greetings)
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", response))
            
            # How are you
            elif any(phrase in user_input.lower() for phrase in ['how are you', "what's up", "how's it going"]):
                response = random.choice(how_are_you_responses)
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", response))
            
            # Jokes
            elif any(word in user_input.lower() for word in ['joke', 'funny', 'laugh']):
                joke = get_joke()
                response = f"[bold]Here's a joke for you:[/bold]\n\n💡 {joke}"
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", "Told a joke"))
            
            # Weather
            elif any(word in user_input.lower() for word in ['weather', 'temperature', 'forecast']):
                weather_report = get_weather()
                response = f"[bold]Weather Report:[/bold]\n\n🌤️  {weather_report}"
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", "Gave weather report"))
            
            # Time
            elif any(word in user_input.lower() for word in ['time', 'clock', 'hour']):
                current_time = time.strftime("%I:%M %p")
                response = f"[bold]Current Time:[/bold]\n\n🕒 It's {current_time}"
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", f"Told time: {current_time}"))
            
            # Quotes
            elif any(word in user_input.lower() for word in ['quote', 'inspire', 'motivation']):
                quote = get_quote()
                response = f"[bold]Inspirational Quote:[/bold]\n\n💫 {quote}"
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", "Shared a quote"))
            
            # Color change
            elif any(word in user_input.lower() for word in ['color', 'theme', 'change color']):
                new_color = random.choice([c for c in color_themes if c != current_color])
                current_color = new_color
                response = f"[bold {new_color}]Color theme changed to {new_color}![/bold {new_color}] ✨"
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", f"Changed color to {new_color}"))
            
            # Thank you
            elif any(word in user_input.lower() for word in ['thank', 'thanks', 'appreciate']):
                response = "[bold]You're welcome![/bold] I'm always happy to help! 😊"
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", response))
            
            # Default response
            else:
                responses = [
                    f"[bold]Hmm, I'm not sure about '{user_input}'[/bold]\n\nTry asking about the [cyan]weather[/cyan], tell me a [green]joke[/green], or ask for a [magenta]quote[/magenta]!",
                    f"[bold]That's interesting: '{user_input}'[/bold]\n\nYou can type [yellow]'help'[/yellow] to see all the things I can do!",
                    f"[bold]I'm still learning about phrases like that![/bold]\n\nMaybe ask me about the [blue]time[/blue] or how I'm [green]feeling[/green] today!"
                ]
                response = random.choice(responses)
                display_chat_message("bot", response, current_color)
                history.append(("Jarvis", "Didn't understand input"))
                
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted by user. Ending chat...[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print("[yellow]Let's continue chatting![/yellow]")

def main():
    """Main function to run the chatbot"""
    try:
        chatbot_with_rich()
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
        console.print("[yellow]Please make sure you have the Rich library installed:[/yellow]")
        console.print("[cyan]pip install rich[/cyan]")

if __name__ == "__main__":
    # Check if Rich is installed
    try:
        from rich import print
        main()
    except ImportError:
        console.print("[red]Error: Rich library is not installed![/red]")
        console.print("Please install it using: [cyan]pip install rich[/cyan]")
        sys.exit(1)
        