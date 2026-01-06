# Contributing to ForestGuard AI

Thank you for your interest in contributing to ForestGuard AI! 🌲

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/forestguard-ai.git
   cd forestguard-ai
   ```
3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Adding New Countries
To add a new country to the dashboard:

1. **Add country data** in `src/dashboard_clean.py`:
   ```python
   "New Country": {
       "bounds": [[lat_min, lon_min], [lat_max, lon_max]],
       "polygon": [(lon1, lat1), (lon2, lat2), ...],
       "deforestation_zones": [
           {"center": (x, y), "name": "Zone Name", "intensity": 0.8, "size": 30},
           # Add more zones...
       ]
   }
   ```

2. **Test the new country**:
   ```bash
   python run_app.py
   ```

### Performance Guidelines
- Keep zone sizes ≤ 40 pixels for optimal performance
- Use NumPy operations for data processing
- Limit the number of zones per country (5-20 recommended)

## 🐛 Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## 💡 Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Describe the use case
- Explain why it would be valuable
- Consider implementation complexity

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Test your changes thoroughly
   - Update documentation if needed

3. **Commit your changes**
   ```bash
   git commit -m "Add: descriptive commit message"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit pull request**
   - Describe your changes
   - Reference any related issues
   - Include screenshots for UI changes

## 🧪 Testing

Before submitting:
- Test the application locally
- Verify all countries load correctly
- Check performance with different resolutions
- Test both legal and illegal deforestation modes

## 📚 Documentation

Help improve our documentation:
- Fix typos and unclear explanations
- Add examples and use cases
- Improve code comments
- Update README for new features

## 🌍 Data Contributions

We welcome contributions of:
- New country boundary data
- Realistic deforestation zone locations
- Updated forest coverage information
- Performance optimizations

## 📞 Questions?

- Open an issue for questions
- Join our discussions
- Check existing documentation

## 🙏 Recognition

Contributors will be:
- Listed in our contributors section
- Mentioned in release notes
- Credited for significant contributions

Thank you for helping make ForestGuard AI better! 🌲✨