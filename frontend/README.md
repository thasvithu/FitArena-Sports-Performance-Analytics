# FitArena Frontend

Modern Vue.js 3 + Vuetify 3 frontend for the FitArena Sports Performance Analytics Platform.

## 🎨 Features

- **Modern UI/UX** - Beautiful Material Design with Vuetify 3
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Real-time Analytics** - Interactive charts and visualizations with ApexCharts
- **Dark Mode** - Toggle between light and dark themes
- **Role-based Access** - Different views for athletes, coaches, and admins
- **AI Recommendations** - Display personalized recommendations with priority indicators
- **Performance Predictions** - Visualize future performance with confidence intervals
- **Team Management** - Manage teams and members
- **Data Upload** - Upload CSV/Excel files for analysis
- **Report Generation** - Create and download performance reports

## 📋 Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running on http://localhost:8000

## 🚀 Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run serve
```

The application will be available at http://localhost:3000

### Build for Production

```bash
npm run build
```

Built files will be in the `dist/` directory.

### Linting

```bash
npm run lint
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
│   └── index.html      # HTML template
├── src/
│   ├── assets/         # Images, fonts, etc.
│   ├── components/     # Reusable Vue components
│   ├── views/          # Page components
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Dashboard.vue
│   │   ├── Analytics.vue
│   │   ├── Teams.vue
│   │   ├── TeamDetail.vue
│   │   ├── Recommendations.vue
│   │   ├── Predictions.vue
│   │   ├── DataUpload.vue
│   │   ├── Reports.vue
│   │   ├── Profile.vue
│   │   └── NotFound.vue
│   ├── router/         # Vue Router configuration
│   │   └── index.js
│   ├── store/          # Vuex state management
│   │   ├── index.js
│   │   └── modules/
│   │       ├── auth.js
│   │       ├── analytics.js
│   │       ├── teams.js
│   │       └── notifications.js
│   ├── services/       # API services
│   │   ├── api.js
│   │   └── authService.js
│   ├── utils/          # Helper functions
│   ├── plugins/        # Vue plugins
│   │   └── vuetify.js
│   ├── App.vue         # Root component
│   └── main.js         # Application entry point
├── .env.development    # Development environment variables
├── .env.production     # Production environment variables
├── package.json        # Dependencies
├── vue.config.js       # Vue CLI configuration
└── .eslintrc.js        # ESLint configuration
```

## 🎯 Key Components

### Views

- **Login/Register** - Authentication pages with form validation
- **Dashboard** - KPI cards, activity trends, performance charts
- **Analytics** - Advanced analytics with comparison, correlation, distribution analysis
- **Teams** - Team management with CRUD operations
- **Recommendations** - AI-powered recommendations with priority filtering
- **Predictions** - Performance predictions with confidence intervals
- **Data Upload** - File upload with validation and history
- **Reports** - Generate and download reports
- **Profile** - User profile and settings

### State Management (Vuex)

- **auth** - Authentication state, login/logout, user info
- **analytics** - Analytics data, trends, summaries
- **teams** - Team management state
- **notifications** - Global notification system

### Services

- **api.js** - Axios instance with interceptors
- **authService.js** - All API calls (auth, users, teams, analytics, etc.)

## 🔧 Configuration

### Environment Variables

Create `.env.development` and `.env.production` files:

```env
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
VUE_APP_TITLE=FitArena
VUE_APP_ENV=development
```

### API Proxy

The development server proxies API requests to the backend:

```javascript
// vue.config.js
devServer: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## 🎨 Theming

Themes are configured in `src/plugins/vuetify.js`:

```javascript
const customTheme = {
  dark: false,
  colors: {
    primary: '#1976D2',
    secondary: '#424242',
    accent: '#82B1FF',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107'
  }
}
```

## 🔐 Authentication

### Login Flow

1. User enters credentials
2. API returns JWT token
3. Token stored in localStorage
4. Token included in all subsequent requests
5. Router guards protect authenticated routes

### Protected Routes

```javascript
meta: { 
  requiresAuth: true,
  roles: ['coach', 'admin']  // Optional role restriction
}
```

## 📊 Charts & Visualizations

Using **ApexCharts** for all visualizations:

- Line charts - Activity trends, performance over time
- Bar charts - Weekly comparisons
- Donut charts - Activity distribution
- Area charts - Calories, heart rate
- Heatmaps - Correlation analysis
- Box plots - Distribution analysis

## 🚦 Routing

Routes are defined in `src/router/index.js`:

| Route | Component | Access |
|-------|-----------|--------|
| `/login` | Login | Public |
| `/register` | Register | Public |
| `/dashboard` | Dashboard | Authenticated |
| `/analytics` | Analytics | Authenticated |
| `/teams` | Teams | Coach/Admin |
| `/teams/:id` | TeamDetail | Authenticated |
| `/recommendations` | Recommendations | Authenticated |
| `/predictions` | Predictions | Authenticated |
| `/data-upload` | DataUpload | Coach/Admin |
| `/reports` | Reports | Authenticated |
| `/profile` | Profile | Authenticated |

## 📱 Responsive Design

Breakpoints (Vuetify):

- **xs**: < 600px (mobile)
- **sm**: 600px - 960px (tablet)
- **md**: 960px - 1264px (laptop)
- **lg**: 1264px - 1904px (desktop)
- **xl**: > 1904px (large desktop)

## 🧪 Testing

```bash
# Run unit tests
npm run test:unit

# Run with coverage
npm run test:unit -- --coverage
```

## 🎯 Best Practices

1. **Component Structure** - Use composition API where beneficial
2. **State Management** - Keep computed properties for derived state
3. **API Calls** - Always use try-catch with loading states
4. **Error Handling** - Display user-friendly messages
5. **Loading States** - Show spinners during async operations
6. **Form Validation** - Validate on client and server
7. **Responsive** - Test on multiple screen sizes
8. **Accessibility** - Use semantic HTML and ARIA labels

## 🐛 Troubleshooting

### Issue: API calls fail with CORS errors

**Solution**: Ensure backend has correct CORS configuration and proxy is set up in `vue.config.js`

### Issue: Charts not displaying

**Solution**: Check that ApexCharts is installed:
```bash
npm install apexcharts vue3-apexcharts
```

### Issue: Vuetify styles not loading

**Solution**: Ensure Vuetify plugin is properly registered in `main.js`

## 🔄 Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make Changes**
   - Edit components in `src/`
   - Test locally with `npm run serve`

3. **Lint Code**
   ```bash
   npm run lint
   ```

4. **Build & Test**
   ```bash
   npm run build
   ```

5. **Commit & Push**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

## 📦 Deployment

### Using Docker

```bash
# Build image
docker build -t fitarena-frontend .

# Run container
docker run -p 3000:80 fitarena-frontend
```

### Using Nginx

1. Build production files:
   ```bash
   npm run build
   ```

2. Copy `dist/` to Nginx web root:
   ```bash
   cp -r dist/* /var/www/html/
   ```

3. Configure Nginx:
   ```nginx
   server {
     listen 80;
     server_name fitarena.com;
     root /var/www/html;
     
     location / {
       try_files $uri $uri/ /index.html;
     }
     
     location /api {
       proxy_pass http://backend:8000;
     }
   }
   ```

## 🤝 Contributing

1. Follow Vue.js style guide
2. Use Vuetify components consistently
3. Add TypeScript types where beneficial
4. Write unit tests for critical functionality
5. Update documentation

## 📚 Resources

- [Vue.js 3 Documentation](https://vuejs.org/)
- [Vuetify 3 Documentation](https://vuetifyjs.com/)
- [Vue Router Documentation](https://router.vuejs.org/)
- [Vuex Documentation](https://vuex.vuejs.org/)
- [ApexCharts Documentation](https://apexcharts.com/)

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ using Vue.js 3 + Vuetify 3**
