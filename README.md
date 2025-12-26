
# Quiz Tac Toe 🎯

A modern twist on the classic Tic Tac Toe game that combines strategic gameplay with quiz knowledge. Challenge your friends in real-time multiplayer matches where you must answer questions correctly to earn the right to make your move!

## 🎮 Game Modes

### Quiz Multiplayer
Answer trivia questions to earn moves in Tic Tac Toe. Only players who answer correctly can place their X or O on the board!

### Classic Multiplayer
Traditional Tic Tac Toe gameplay with friends in real-time.

### Singleplayer
Challenge yourself against AI.

## 🚀 Features

- **Real-time Multiplayer**: Powered by Socket.IO for instant gameplay
- **Multiple Quiz Categories**: 
  - Mathematics
  - Science
  - Geography
  - History
  - Test Questions
- **User Authentication**: Secure login/registration system
- **Leaderboard**: Track wins and losses across all players
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Timer System**: 30-second countdown adds urgency to each question
- **Futuristic UI**: Stunning visual effects with neon gradients and animations
- **Real-time Notifications**: Get instant feedback on game events

## 🛠️ Technology Stack

- **Backend**: Python Flask with Socket.IO
- **Database**: SQLite for user management and leaderboards
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time Communication**: Socket.IO for multiplayer functionality
- **Styling**: Custom CSS with gradients, animations, and responsive design

## 📋 Prerequisites

- Python 3.7+
- Flask
- Flask-SocketIO
- Werkzeug

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd quiz-tac-toe
```

2. Install dependencies:
```bash
pip install flask flask-socketio werkzeug
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

### First Time Setup

1. Create an account using the registration form
2. Log in with your credentials
3. Choose your game mode and start playing!

## 🎯 How to Play (Quiz Mode)

1. **Create or Join Game**: Start a new game or join using a Game ID
2. **Select Category**: Choose from Math, Science, Geography, or History
3. **Wait for Players**: Game starts when both players join
4. **Answer Questions**: Type your answer and press Enter
5. **Make Your Move**: Answer correctly to earn the right to place X or O
6. **Win the Game**: First to get three in a row wins!

## 🎨 Game Features

### Timer System
- 30-second countdown for each question
- Visual progress bar
- Automatic question reset when time expires

### Real-time Notifications
- Answer feedback (correct/incorrect)
- Player join/leave notifications
- Game status updates

### Responsive Design
- Mobile-friendly interface
- Touch-optimized controls
- Adaptive layouts for all screen sizes

## 🏆 Leaderboard System

Track your progress with the integrated leaderboard:
- Win/Loss statistics
- Player rankings
- Global competition

## 📱 Mobile Support

Fully optimized for mobile devices with:
- Touch-friendly controls
- Responsive grid layout
- Optimized font sizes and spacing
- Mobile-specific CSS media queries

## 🎨 Visual Features

- **Animated Neon Text Effects**: Eye-catching title animations
- **Gradient Backgrounds**: Beautiful color transitions
- **Smooth Hover Animations**: Interactive button effects
- **Real-time Game Updates**: Instant visual feedback
- **Professional Overlays**: Polished game-over screens

## 🔧 Configuration

### Database
The application uses SQLite for user management. The database is automatically initialized on first run.

### Categories
Add new question categories by editing the `quiz_questions` array in `app.py`:

```python
{
    "question": "Your question here?",
    "answer": "correct answer",
    "category": "your_category"
}
```

## 📂 Project Structure

```
quiz-tac-toe/
├── app.py                 # Main Flask application
├── users.db              # SQLite database
├── static/               # Static assets (images)
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── game.html         # Quiz multiplayer game
│   ├── login.html        # Authentication
│   ├── leaderboard.html  # Leaderboard display
│   └── ...
└── README.md            # This file
```

## 🎯 Game Rules

### Quiz Multiplayer
1. Both players see the same question
2. First to answer correctly earns the move
3. Timer resets after each question
4. Players can only attempt each question once
5. Game continues until someone wins or draws

### Classic Multiplayer
1. Traditional turn-based Tic Tac Toe
2. X always goes first
3. Players alternate turns
4. First to get three in a row wins

## 🐛 Troubleshooting

### Common Issues

**Game not loading?**
- Check that both players have joined
- Refresh the page and try again

**Timer not starting?**
- Ensure both players are connected
- Wait for a new question to appear

**Can't join game?**
- Verify the Game ID is correct
- Make sure the game isn't full (2 players max)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Acknowledgments

- Socket.IO for real-time multiplayer functionality
- Flask for the robust web framework
- Google Fonts for typography
- Font Awesome for icons

## Screenshots
  <img width="1920" height="1080" alt="Screenshot 2025-11-14 120046" src="https://github.com/user-attachments/assets/dda9a97d-df2d-4196-8c2c-0a84b34e1f98" />
  <img width="1920" height="1080" alt="Screenshot 2025-11-14 120009" src="https://github.com/user-attachments/assets/874aa1f7-1342-4f99-b667-306329598088" />
<img width="1920" height="1080" alt="Screenshot 2025-11-14 120131" src="https://github.com/user-attachments/assets/fa38d0df-a923-45f1-872e-e2098ce7737a" />
<img width="1920" height="1080" alt="Screenshot 2025-11-14 120151" src="https://github.com/user-attachments/assets/4909ab19-421c-49bf-95a3-c3280c83057c" />
<img width="1920" height="1080" alt="Screenshot 2025-11-14 120211" src="https://github.com/user-attachments/assets/291f035f-b3d4-4780-8cdd-5f023ac077c3" />
<img width="1920" height="1080" alt="Screenshot 2025-11-14 120225" src="https://github.com/user-attachments/assets/154e8943-44dc-4ac1-889c-73e746d64d45" />
<img width="1920" height="1080" alt="Screenshot (210)" src="https://github.com/user-attachments/assets/9889a941-3dbe-42ee-a1ae-5df3a99b0306" />
<img width="1920" height="1080" alt="Screenshot (211)" src="https://github.com/user-attachments/assets/480bf910-653f-40b0-af72-e64777a93e9d" />
<img width="1920" height="1080" alt="Screenshot (212)" src="https://github.com/user-attachments/assets/dee57b86-6bf5-472b-a6f9-1d788f9e608b" />
<img width="1920" height="1080" alt="Screenshot (213)" src="https://github.com/user-attachments/assets/b6333272-e69a-4307-bad8-2bc658d6d984" />
<img width="1920" height="1080" alt="Screenshot (214)" src="https://github.com/user-attachments/assets/2f75a6cd-cf47-4725-b78d-3f2f338207d5" />
<img width="1920" height="1080" alt="Screenshot (215)" src="https://github.com/user-attachments/assets/858ec4c0-0a4b-47e0-b10d-d8a279c70321" />



## 📞 Support

If you encounter any issues or have questions, please create an issue in the repository.

---

**Enjoy playing Quiz Tac Toe!** 🎮✨
