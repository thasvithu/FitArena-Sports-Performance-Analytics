# FitArena Frontend - Quick Start Guide

## 🚀 Get Your Frontend Running in 3 Minutes

### Step 1: Install Dependencies (1 minute)

```powershell
# Navigate to frontend directory
cd frontend

# Install all dependencies
npm install
```

### Step 2: Configure Environment (30 seconds)

The `.env.development` file is already configured for local development:

```env
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
VUE_APP_TITLE=FitArena - Development
VUE_APP_ENV=development
```

### Step 3: Start Development Server (30 seconds)

```powershell
# Start the dev server
npm run serve
```

Frontend will be available at: **http://localhost:3000**

---

## 📱 What You'll See

### 1. Login Page (http://localhost:3000/login)

- Beautiful Material Design login form
- Form validation
- Link to registration page

**Test Credentials** (after backend is running):
- Username: `testuser`
- Password: `password123`

### 2. Registration Page (http://localhost:3000/register)

- Multi-step registration form
- Role selection (Athlete/Coach)
- Email validation
- Password strength checking

### 3. Dashboard (http://localhost:3000/dashboard)

After login, you'll see:

- **4 KPI Cards**: Steps, Calories, Active Minutes, Performance Score
- **Activity Trends Chart**: 30-day line chart with multiple metrics
- **Activity Distribution**: Donut chart showing workout types
- **Weekly Performance**: Bar chart with daily scores
- **Calories Burned**: Area chart with gradient
- **Recent Activity Table**: Last 5 activities with intensity

### 4. Analytics Page (http://localhost:3000/analytics)

- **Performance Comparison**: Current vs Previous period
- **Correlation Heatmap**: Relationship between metrics
- **Distribution Analysis**: Box plot charts
- **Statistical Summary Table**: Mean, Min, Max, Std Dev
- **Export Options**: PDF and Excel export

### 5. Teams Page (http://localhost:3000/teams)

*Available for Coach/Admin roles only*

- Team cards with member counts
- Create/Edit/Delete teams
- Team performance metrics
- Click to view team details

### 6. Recommendations Page (http://localhost:3000/recommendations)

- AI-powered recommendations with priorities
- Action items checklist
- Expected impact predictions
- Confidence scores
- Filter by priority (High/Medium/Low)

### 7. Predictions Page (http://localhost:3000/predictions)

- Performance forecasts with ML models
- Historical vs Predicted data charts
- Confidence intervals
- Model accuracy metrics
- Predicted goals with probability

### 8. Data Upload (http://localhost:3000/data-upload)

*Available for Coach/Admin roles only*

- Drag & drop file upload
- CSV and Excel support
- Upload history table
- Data validation

### 9. Reports Page (http://localhost:3000/reports)

- Generate custom reports
- Choose report type, period, format
- Download existing reports
- Report history

### 10. Profile Page (http://localhost:3000/profile)

- Edit user information
- Change password
- View role and permissions

---

## 🎨 Features to Explore

### Dark Mode Toggle

Click the **brightness icon** in the top-right app bar to switch between light and dark themes.

### Navigation

- **Desktop**: Permanent sidebar navigation
- **Mobile/Tablet**: Hamburger menu (top-left)

### Responsive Design

Try resizing your browser or opening on mobile:
- Layouts adapt automatically
- Charts scale responsively
- Tables become scrollable
- Mobile-optimized forms

---

## 🔗 Connect to Backend

### Prerequisites

Make sure your backend is running:

```powershell
# In another terminal, from project root
cd src/api
python main.py
```

Backend should be at: **http://localhost:8000**

### API Connection

The frontend automatically connects to the backend via proxy configuration in `vue.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

All API calls to `/api/*` are forwarded to the backend.

---

## 🧪 Test the Complete Flow

### 1. Register a New User

```
1. Go to http://localhost:3000/register
2. Fill in:
   - Username: john_athlete
   - Email: john@example.com
   - Password: securepass123
   - Confirm Password: securepass123
   - Role: Athlete
3. Click "Register"
```

### 2. Login

```
1. Redirected to login automatically
2. Enter credentials from registration
3. Click "Login"
```

### 3. Explore Dashboard

```
1. View KPI cards with your stats
2. Interact with charts (hover, zoom)
3. Check recent activity table
```

### 4. Generate Recommendations

```
1. Navigate to Recommendations page
2. Click "Generate New" button
3. View AI-powered suggestions
4. Filter by priority
```

### 5. Make Predictions

```
1. Navigate to Predictions page
2. Select metric (Steps, Calories, etc.)
3. Choose prediction period
4. Click "Generate Prediction"
5. View forecasted data
```

---

## 📊 Sample Data

The frontend includes sample data for development:

- **Dashboard**: 30 days of activity data
- **Analytics**: Correlation matrices, statistical summaries
- **Teams**: 3 sample teams (Elite Runners, Power Lifters, Cardio Warriors)
- **Recommendations**: 5 sample recommendations with various priorities
- **Predictions**: Historical and predicted data charts

This allows you to see the UI immediately without backend data.

---

## 🎯 Navigation Menu

| Menu Item | Icon | Description |
|-----------|------|-------------|
| Dashboard | 📊 | Performance overview and KPIs |
| Analytics | 📈 | Advanced analytics and comparisons |
| Teams* | 👥 | Team management (Coach/Admin) |
| Recommendations | 💡 | AI-powered suggestions |
| Predictions | 🔮 | Performance forecasts |
| Reports | 📄 | Generate and download reports |
| Data Upload* | ⬆️ | Upload CSV/Excel files (Coach/Admin) |

*Visible only for Coach/Admin roles

---

## 🔧 Common Tasks

### Change API URL

Edit `frontend/.env.development`:

```env
VUE_APP_API_BASE_URL=http://your-api-url:8000/api/v1
```

Restart dev server after changes.

### Add New Chart

```vue
<template>
  <apexchart
    type="line"
    :options="chartOptions"
    :series="chartSeries"
  />
</template>

<script>
export default {
  data() {
    return {
      chartOptions: { /* config */ },
      chartSeries: [{ name: 'Data', data: [...] }]
    }
  }
}
</script>
```

### Call API Endpoint

```javascript
import authService from '@/services/authService'

// Get analytics
const data = await authService.getAnalyticsSummary(athleteId, {
  period: '30days'
})

// Generate recommendations
const recs = await authService.generateRecommendations(athleteId)

// Upload file
const formData = new FormData()
formData.append('file', file)
await authService.uploadData(formData)
```

---

## 🐛 Troubleshooting

### Frontend won't start

```powershell
# Clear node_modules and reinstall
rm -r node_modules
rm package-lock.json
npm install
```

### API calls fail

1. Check backend is running: http://localhost:8000
2. Check browser console for errors
3. Verify proxy configuration in `vue.config.js`
4. Check CORS settings in backend

### Charts not displaying

```powershell
# Reinstall ApexCharts
npm install apexcharts vue3-apexcharts --save
```

### Authentication issues

1. Clear localStorage: Browser DevTools > Application > Local Storage > Clear
2. Re-login
3. Check token in Network tab

---

## 📱 Mobile Testing

### Using Chrome DevTools

1. Open browser DevTools (F12)
2. Click device toolbar icon (Ctrl+Shift+M)
3. Select device (iPhone, iPad, etc.)
4. Test responsiveness

### Recommended Test Devices

- iPhone 12 Pro (390x844)
- iPad Air (820x1180)
- Samsung Galaxy S20 (360x800)

---

## 🎨 Customize Theme

Edit `frontend/src/plugins/vuetify.js`:

```javascript
const customTheme = {
  dark: false,
  colors: {
    primary: '#YOUR_COLOR',    // Change primary color
    secondary: '#YOUR_COLOR',  // Change secondary color
    // ... other colors
  }
}
```

Restart dev server to see changes.

---

## 📦 Build for Production

```powershell
# Create optimized production build
npm run build

# Output will be in dist/ directory
# Ready to deploy to web server
```

---

## 🎓 Next Steps

1. **Explore all pages** - Click through every menu item
2. **Test responsive design** - Resize browser window
3. **Try dark mode** - Toggle theme switcher
4. **Connect to backend** - Ensure API integration works
5. **Customize theme** - Change colors to match your brand
6. **Add real data** - Replace sample data with API calls

---

## 📚 Learn More

- Review `frontend/README.md` for detailed documentation
- Check Vue.js 3 docs: https://vuejs.org/
- Vuetify 3 components: https://vuetifyjs.com/
- ApexCharts examples: https://apexcharts.com/

---

**Enjoy building with FitArena! 🏃‍♂️📊**
