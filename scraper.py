import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_afedne():
    url = "https://qa.afedne.com/"
    
    # تعريف هوية المتصفح (User-Agent) لكي يرحب بنا الموقع ولا يحظرنا
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # تحليل كود HTML للصفحة
        soup = BeautifulSoup(response.text, 'html.parser')
        feed_items = []
        
        # البحث عن جميع الروابط في الصفحة
        for link in soup.find_all('a'):
            href = link.get('href')
            title = link.get_text(strip=True)
            
            # فلترة ذكية: نأخذ فقط الروابط التي عنوانها أطول من 15 حرف (لتجنب روابط القوائم الجانبية)
            if href and title and len(title) > 15:
                # تحويل الروابط المختصرة إلى روابط كاملة لتعمل في تطبيقك
                if not href.startswith('http'):
                    href = f"https://qa.afedne.com/{href.lstrip('/')}"
                
                # استبعاد روابط السوشيال ميديا
                if "facebook" not in href and "twitter" not in href and "whatsapp" not in href:
                    # التأكد من عدم تكرار نفس المقال في الـ Feed
                    if not any(item['link'] == href for item in feed_items):
                        feed_items.append({
                            "title": title,
                            "link": href,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
        
        # حفظ البيانات المستخرجة في ملف JSON
        with open('feed.json', 'w', encoding='utf-8') as f:
            json.dump({
                "status": "success",
                "source": "منصة أفدني - قطر",
                "total_items": len(feed_items),
                "items": feed_items
            }, f, ensure_ascii=False, indent=4)
            
        print(f"✅ تم بنجاح سحب {len(feed_items)} مقال وتحديث الـ Feed!")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء سحب البيانات: {e}")

if __name__ == "__main__":
    scrape_afedne()
