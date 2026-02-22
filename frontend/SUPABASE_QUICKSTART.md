# 🚀 Supabase Setup Guide for Ivy Wealth AI

## Quick Setup (5 minutes)

### Step 1: Create a Supabase Project
1. Go to [https://app.supabase.com](https://app.supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Name it: `ivy-wealth-ai`
5. Create a strong password and select your region
6. Wait for the project to initialize (~1 minute)

### Step 2: Create Database Table
1. Go to the SQL Editor in your Supabase project
2. Click "New Query"
3. **Copy and paste the entire contents of `SUPABASE_SETUP.sql`** into the editor
4. Click "Run" to execute the SQL
5. Wait for completion - you should see ✓ messages

**The SQL script will:**
- Create a `clients` table with all required fields
- Enable Row Level Security (RLS) for data access
- Insert 50 sample clients with realistic data
- Create indexes for fast queries

### Step 3: Get Your API Credentials

1. In your Supabase project, go to **Settings** > **API**
2. Copy your **Project URL** (looks like: `https://xxxx.supabase.co`)
3. Copy your **anon key** (public key for client-side access)

### Step 4: Configure React Frontend

1. In the `frontend` folder, create a file named `.env.local` with:

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
VITE_API_BASE=http://localhost:8000/api
```

Replace the values with your actual Supabase credentials!

### Step 5: Start the Frontend
```bash
cd frontend
npm run dev
```

The app will now:
- ✅ Load real data from Supabase
- ✅ Show 50 sample clients
- ✅ Display interactive charts
- ✅ Filter and search clients
- ✅ Generate AI reports for each client

## Verification

After setup, you should see:
1. **50 clients listed** in the Clients tab
2. **Interactive charts** in the Analytics tab showing:
   - Client status distribution (pie chart)
   - Risk tolerance distribution (pie chart)
   - Portfolio value ranges (bar chart)
3. **Search and filter** working for clients
4. **Client detail modal** opening when clicking on a client

## Troubleshooting

### "Failed to connect to Supabase"
- Verify your `.env.local` credentials are correct
- Ensure VITE_ prefix is used for environment variables
- Check that the Supabase project is active

### Still seeing mock data instead of Supabase data
- The app is configured to fall back to mock data if Supabase is not available
- Check browser console (F12) for errors
- Verify the SQL table was created in Supabase

### API calls failing
- Ensure backend API is running: `python app.py` in the `rohith` folder
- Check that CORS is enabled (already configured in FastAPI)

## Features Included

### 🎨 Beautiful UI
- Glass-morphism dark theme with blue gradients
- Responsive grid layout for all screen sizes
- Smooth transitions and hover effects

### 📊 Advanced Analytics
- Status distribution (On Track, At Risk, Needs Review)
- Risk tolerance breakdown (Conservative, Moderate, Aggressive)
- Portfolio value ranges visualization
- Key metrics cards with percentages

### 🔍 Search & Filter
- Search by client name or email
- Filter by risk tolerance level
- Filter by status
- Real-time filtering updates

### 💬 Client Details
- Click any client card to see a detailed modal
- View full client information
- See portfolio progress percentage
- Generate AI reports directly from the modal

### 📈 Charts & Visualizations
- Pie charts for status and risk distribution
- Bar chart for portfolio value ranges
- Interactive tooltips and legends
- Responsive chart sizing

### 🤖 AI Integration
- Generate personalized wealth reports
- Integration with backend LangGraph pipeline
- Support for multiple LLM providers (OpenRouter, Groq, Google Gemini)

## Database Schema

The `clients` table includes:
- `id` (Primary Key)
- `client_id` (Unique identifier: CLIENT_001, CLIENT_002, etc.)
- `name` (Client full name)
- `email` (Client email address)
- `portfolio_value` (Current portfolio value in dollars)
- `risk_tolerance` (Conservative, Moderate, or Aggressive)
- `goal_amount` (Target portfolio value)
- `status` (On Track, At Risk, or Needs Review)
- `last_report` (Date of last generated report)
- `created_at` (Timestamp when record was created)
- `updated_at` (Timestamp when record was last updated)

## Sample Data

The setup includes 50 sample clients with:
- Diverse names and emails
- Portfolio values ranging from $100K to $1.1M
- Mix of risk tolerance levels
- Various status indicators
- Recent report dates

## Next Steps

1. **Deploy to Production** (optional)
   - Deploy Supabase project (free tier available)
   - Deploy React frontend (Vercel, Netlify, etc.)
   - Update API endpoints for production

2. **Add More Clients**
   - Use Supabase dashboard to add more clients
   - Or write a script to bulk import client data

3. **Customize Reports**
   - Modify the backend report generation
   - Add more analysis metrics
   - Include portfolio recommendations

4. **Advanced Features**
   - Real-time notifications for at-risk portfolios
   - Historical report tracking
   - Client communication templates
   - Export reports to PDF

## Support

If you encounter any issues:
1. Check the browser console (F12) for error messages
2. Verify all environment variables are set correctly
3. Ensure the backend API is running and accessible
4. Check Supabase project status and API availability

Good luck with your hackathon submission! 🎉
