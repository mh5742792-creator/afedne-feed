import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_afedne_categorized():
    # هنا تضع التصنيفات التي تريدها والروابط الخاصة بها
    categories = {
        "عربي_ثاني_عشر_فصل_ثاني": "https://qa.afedne.com/library?level_id=4&division_id=14&term_id=2&subject_id=211&content_id=1",
        # يمكنك إضافة أي روابط أخرى هنا بنفس الطريقة، مثال:
        # "فيزياء_عاشر": "رابط قسم الفيزياء هنا",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    final_feed = {
        "status": "success",
        "source": "منصة أفدني - قطر",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": {} # سيتم حفظ كل قسم هنا
    }
    
    for category_name, category_url in categories.items():
        print(f"جاري سحب بيانات قسم: {category_name} ...")
        category_items = []
        
        try:
            response = requests.get(category_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                title = link.get('title') or link.get_text(strip=True)
                
                # فلترة دقيقة: نأخذ فقط الروابط التي تؤدي إلى ملفات/مذكرات
                if href and '/library/file/' in href and title:
                    if not href.startswith('http'):
                        href = f"https://qa.afedne.com{href}"
                    
                    # منع التكرار داخل نفس القسم
                    if not any(item['link'] == href for item in category_items):
                        category_items.append({
                            "title": title,
                            "link": href
                        })
            
            final_feed["categories"][category_name] = category_items
            print(f"✅ تم العثور على {len(category_items)} ملف في {category_name}")
            
        except Exception as e:
            print(f"❌ خطأ في قسم {category_name}: {e}")
            final_feed["categories"][category_name] = [] # نضع قائمة فارغة في حال حدوث خطأ

    # حفظ البيانات المجمعة
    with open('feed.json', 'w', encoding='utf-8') as f:
        json.dump(final_feed, f, ensure_ascii=False, indent=4)
        
    print("✅ تم تحديث ملف الـ JSON الشامل بنجاح!")

if __name__ == "__main__":
    scrape_afedne_categorized()
