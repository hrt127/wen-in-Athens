# 🏛️ Production Guide: Temple of Greeks

**Path to Horny Land: Complete deployment guide**

---

## 🔗 Part 1: Clean Up Duplicate Files (Symlinks)

### Problem
You have 3 files duplicated from `elfa-tools`:
- `elfa_client.py`
- `decision_moment.py`
- `narrative_radar.py`

These exist in both the root AND `streamlit/` directory.

### Solution: Use Git Submodules (Better than Symlinks)

Symlinks don't work well in deployed environments. Instead:

#### Option A: Git Submodule (Recommended)
```bash
# Add elfa-tools as a submodule
cd wen-in-Athens
git submodule add https://github.com/YourOrg/elfa-tools.git external/elfa-tools

# Update streamlit imports
# In streamlit/app.py, change:
# from elfa_client import ElfaClient
# to:
import sys
sys.path.insert(0, '../external/elfa-tools')
from elfa_client import ElfaClient
```

#### Option B: Simple Copy (Current - Works for Now)
Keep the copied files in `streamlit/` for now. They're small and won't change often.

**Recommendation:** Option B for quick deployment, Option A for long-term maintenance.

---

## 🧪 Part 2: Test ELFA Client Integration

### What You Need
1. **ELFA API Key** from devs
2. **Test JSON Response** from devs
3. **Streamlit Secrets** configuration

### Setup ELFA Testing

#### 1. Create `.streamlit/secrets.toml` (Local Testing)
```toml
ELFA_API_KEY = "your-api-key-here"
```

#### 2. Test ELFA Client Locally
Create `test_elfa.py` in `streamlit/`:

```python
from elfa_client import ElfaClient
import json

# Test with your JSON
test_response = '''
{
  "BTC": {
    "price": 95000,
    "sentiment": "bullish",
    "momentum": 0.75,
    "themes": ["ETF inflows", "Halving anticipation"],
    "volatility": {
      "implied": 0.65,
      "realized": 0.52
    }
  }
}
'''

# Initialize client
client = ElfaClient(api_key="test-key")

# Test with mock data
test_data = json.loads(test_response)
print("✅ ELFA data structure:")
print(json.dumps(test_data, indent=2))

# Verify expected fields
assert 'BTC' in test_data
assert 'sentiment' in test_data['BTC']
print("\n✅ All fields present!")
```

Run: `python streamlit/test_elfa.py`

#### 3. Test in Streamlit App
```bash
cd streamlit
streamlit run app.py
```

Click "🔄 Refresh Narratives" and check console for:
- ✅ API connection successful
- ✅ Data parsing works
- ✅ Narratives display correctly

#### 4. Configure for Streamlit Cloud
In Streamlit Cloud dashboard:
1. Go to **Settings > Secrets**
2. Add:
```toml
ELFA_API_KEY = "your-production-api-key"
```

### Debugging ELFA Issues

**Problem: "ELFA API key not configured"**
```python
# In streamlit/app.py, add debug:
st.write(f"API Key present: {bool(st.secrets.get('ELFA_API_KEY'))}")
```

**Problem: JSON parsing fails**
```python
# Add try/catch in elfa_client.py:
try:
    data = response.json()
except json.JSONDecodeError as e:
    st.error(f"JSON Error: {e}")
    st.code(response.text)  # Show raw response
```

**Problem: Synthetic data always shows**
This is fine! App works without ELFA API.

---

## 🌐 Part 3: Farcaster Frame Manifest

### Farcaster Frame Requirements

Farcaster Frames need specific `<meta>` tags in your HTML. Since this is a Streamlit app, we'll create a **frame endpoint** that Warpcast can embed.

### What Farcaster Needs

1. **Frame Metadata** - Special meta tags
2. **Image Preview** - OG image for frame
3. **Action Buttons** - Interactive buttons
4. **Post URL** - Where button clicks go

### Implementation

#### Option A: Simple Cast (No Frame - Easiest)
Just post text casts with links (what we built). ✅ Already works!

#### Option B: Full Frame Integration (Advanced)

Create `streamlit/frame.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <meta property="fc:frame" content="vNext" />
  <meta property="fc:frame:image" content="https://your-app.streamlit.app/frame-image.png" />
  <meta property="fc:frame:button:1" content="Enter Temple" />
  <meta property="fc:frame:button:1:action" content="link" />
  <meta property="fc:frame:button:1:target" content="https://your-app.streamlit.app" />
  
  <meta property="og:title" content="Temple of Greeks 🏛️" />
  <meta property="og:description" content="Learn options Greeks through absurd philosopher commentary" />
  <meta property="og:image" content="https://your-app.streamlit.app/og-image.png" />
</head>
<body>
  <h1>Temple of Greeks</h1>
  <p>Redirecting to app...</p>
</body>
</html>
```

#### Create Frame Image

1. Design a 1200x630px image:
   - Temple background
   - "Wen in Athens: Temple of Greeks"
   - Philosopher silhouettes
   - "Learn Greeks through orgies"

2. Host it:
   ```bash
   # Add to streamlit/static/frame-image.png
   # Streamlit will serve it automatically
   ```

### Farcaster Developer Checklist

From Farcaster docs (docs.farcaster.xyz):

✅ **Meta Tags Required:**
- `fc:frame` - Frame version
- `fc:frame:image` - Preview image URL
- `fc:frame:button:1` - At least one button
- `og:title` - Title
- `og:image` - OG image

✅ **Image Requirements:**
- Format: PNG, JPG, or GIF
- Max size: 10MB
- Aspect ratio: 1.91:1 (recommended: 1200x630)

✅ **Button Actions:**
- `link` - Opens URL
- `post` - Posts to your endpoint
- `mint` - Mints NFT

### Testing Farcaster Frames

1. **Use Frame Validator**: https://warpcast.com/~/developers/frames
2. **Paste your URL**: `https://your-app.streamlit.app`
3. **Check validation**: All required tags present?

### Simplified Approach (Recommended)

**Skip full Frame integration for now.**

Instead:
1. ✅ Use the Farcaster client we built (works!)
2. ✅ Post text casts with app links
3. ✅ Users click link → opens Streamlit app
4. Later: Add Frame if you want in-feed interactivity

---

## 🚀 Part 4: Complete Deployment Checklist

### Pre-Deployment

- [ ] Test ELFA integration locally
- [ ] Verify Farcaster casting works (with/without credentials)
- [ ] Test tutorial system
- [ ] Verify all philosopher quotes display
- [ ] Check cult rank progression

### Deploy to Streamlit Cloud

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for production"
git push origin main
```

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Click "New app"**

4. **Configure:**
   - Repo: `hrt127/wen-in-Athens`
   - Branch: `main`
   - Main file: `streamlit/app.py`
   - App URL: `temple-of-greeks` (or your choice)

5. **Add Secrets:**
```toml
ELFA_API_KEY = "your-key"
NEYNAR_API_KEY = "your-neynar-key"
FARCASTER_SIGNER_UUID = "your-signer-uuid"
```

6. **Deploy!** → Wait 2-3 mins

### Post-Deployment

- [ ] Test live app at `https://temple-of-greeks.streamlit.app`
- [ ] Refresh ELFA narratives
- [ ] Test Farcaster casting
- [ ] Complete a full trade cycle
- [ ] Share first cast to `/greeks` channel

---

## 🎯 Quick Start Commands

```bash
# Local testing
cd streamlit
pip install -r requirements.txt
streamlit run app.py

# Test ELFA
python test_elfa.py

# Deploy
git push origin main
# Then use Streamlit Cloud UI
```

---

## 🆘 Troubleshooting

### ELFA Not Connecting
1. Check API key in secrets
2. Look at Streamlit logs (click "Manage app" > "Logs")
3. Synthetic data is fine for testing

### Farcaster Not Posting
1. Verify Neynar credentials
2. Check cast preview shows correctly
3. Test without credentials (shows helpful message)

### App Won't Deploy
1. Check requirements.txt has all dependencies
2. Verify main file path is `streamlit/app.py`
3. Look at deploy logs for errors

---

## 🏁 Final Steps to Horny Land

1. ✅ Deploy to Streamlit Cloud
2. ✅ Test with real trades
3. ✅ Get ELFA + Farcaster credentials
4. ✅ Cast first philosopher roast
5. ✅ Share in `/greeks` channel
6. 🎉 Watch newbies learn Greeks through absurdity

**You're ready! The Temple awaits. May Dionysus bless your casts. 🏛️🔥**
