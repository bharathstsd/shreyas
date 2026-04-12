from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from .models import Invite



def invite_form(request):
    return render(request, "invites/form.html")
# def generate_invite(request):
#     import time
#     from PIL import Image, ImageDraw, ImageFont

#     name = request.POST.get("customer_name", "Customer")

#     # Create a fresh image (no template)
#     img = Image.new("RGB", (1080, 1920), color="#f3a9bc")
#     draw = ImageDraw.Draw(img)

#     font = ImageFont.load_default()

#     # Draw large text
#     draw.text((100, 300), "BBT INVITE", fill="black", font=font)
#     draw.text((100, 400), f"Dear {name}", fill="black", font=font)
#     draw.text((100, 500), "You are invited!", fill="black", font=font)

#     filename = f"fresh_invite_{int(time.time())}.jpg"
#     output_path = os.path.join(settings.MEDIA_ROOT, filename)
#     img.save(output_path)

#     invite_url = settings.MEDIA_URL + filename

#     return JsonResponse({
#         "image": invite_url,
#         "whatsapp": "#"
#     })
def generate_invite(request):
    import time
    from PIL import Image, ImageDraw, ImageFont

    name = request.POST.get("customer_name", "Customer")
    coach = request.POST.get("coach_name", "Coach")
    phone = request.POST.get("coach_phone", "")
    date = request.POST.get("event_date")
    time_val = request.POST.get("event_time")

    # Load template
    template_path = os.path.join(settings.MEDIA_ROOT, "bbt_template.png")
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Load logo
    logo_path = os.path.join(settings.MEDIA_ROOT, "bbtlogo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((300, 150))
        img.paste(logo, (390, 80), logo)

    # Fonts
    font_path = "C:/Windows/Fonts/arial.ttf"
    title_font = ImageFont.truetype(font_path, 70)
    text_font = ImageFont.truetype(font_path, 50)
    small_font = ImageFont.truetype(font_path, 45)

    # Text color (deep rose)
    color = "#5a2d3c"

    # Draw text
    draw.text((120, 400), f"Dear {name},", fill=color, font=title_font)
    draw.text((120, 520), "You are invited for a", fill=color, font=text_font)
    draw.text((120, 600), "complimentary beauty consultation.", fill=color, font=text_font)

    y = 760
    if date:
        draw.text((120, y), f"Date: {date}", fill=color, font=small_font)
        y += 70
    if time_val:
        draw.text((120, y), f"Time: {time_val}", fill=color, font=small_font)
        y += 70

    draw.text((120, y + 40), "Invited by:", fill=color, font=small_font)
    draw.text((120, y + 110), coach, fill=color, font=text_font)
    draw.text((120, y + 180), phone, fill=color, font=small_font)

    # Save
    filename = f"invite_{int(time.time())}.jpg"
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    img.save(output_path, quality=95)

    invite_url = settings.MEDIA_URL + filename

    return JsonResponse({
        "image": invite_url,
        "whatsapp": "#"
    })



# def generate_invite(request):
#     name = request.POST.get("customer_name")
#     customer_phone = request.POST.get("customer_phone")
#     coach = request.POST.get("coach_name")
#     phone = request.POST.get("coach_phone")
#     date = request.POST.get("event_date")
#     time = request.POST.get("event_time")

#     template_path = os.path.join(settings.MEDIA_ROOT, "invite_template.png")
#     img = Image.open(template_path).convert("RGB")
#     draw = ImageDraw.Draw(img)

#     # Use default font (larger text positions)
#     font_large = ImageFont.load_default()
#     font_medium = ImageFont.load_default()
#     font_small = ImageFont.load_default()

#     width, height = img.size
#     center_x = width // 2

#     # Helper function to center text
#     def draw_centered(text, y, font, color):
#         text_width = draw.textlength(text, font=font)
#         x = center_x - text_width // 2
#         draw.text((x, y), text, fill=color, font=font)

#     # Main text
#     draw_centered(f"Dear {name},", 700, font_large, "#5A2E3B")
#     draw_centered("You are invited for a", 760, font_medium, "#5A2E3B")
#     draw_centered("complimentary beauty consultation.", 800, font_medium, "#5A2E3B")

#     y = 900
#     if date:
#         draw_centered(f"Date: {date}", y, font_small, "#5A2E3B")
#         y += 40
#     if time:
#         draw_centered(f"Time: {time}", y, font_small, "#5A2E3B")
#         y += 40

#     draw_centered("Invited by:", y + 20, font_small, "#5A2E3B")
#     draw_centered(coach, y + 60, font_medium, "#5A2E3B")
#     draw_centered(phone, y + 100, font_small, "#5A2E3B")

#     # Save image
#     filename = f"invite_{name.replace(' ', '_')}.jpg"
#     output_path = os.path.join(settings.MEDIA_ROOT, filename)
#     img.save(output_path, quality=95)

#     invite_url = settings.MEDIA_URL + filename
#     whatsapp_link = f"https://wa.me/{customer_phone}"

#     return JsonResponse({
#         "image": invite_url,
#         "whatsapp": whatsapp_link
#     })

# def generate_invite(request):
#     name = request.POST.get("customer_name")
#     coach = request.POST.get("coach_name")
#     phone = request.POST.get("coach_phone")
#     date = request.POST.get("event_date")
#     time = request.POST.get("event_time")
#     customer_phone = request.POST.get("customer_phone")
#     whatsapp_link = f"https://wa.me/{customer_phone}"



#     # Load template
#     template_path = os.path.join(settings.MEDIA_ROOT, "invite_template.png")
#     img = Image.open(template_path).convert("RGB")
#     draw = ImageDraw.Draw(img)

#     # Use default font if custom not available
#     font = ImageFont.load_default()

#     # Draw text
#     draw.text((100, 600), f"Dear {name},", fill="black", font=font)
#     draw.text((100, 700), "You are invited for a beauty consultation.", fill="black", font=font)

#     y = 800
#     if date:
#         draw.text((100, y), f"Date: {date}", fill="black", font=font)
#         y += 50
#     if time:
#         draw.text((100, y), f"Time: {time}", fill="black", font=font)
#         y += 50

#     draw.text((100, y + 40), "Invited by:", fill="black", font=font)
#     draw.text((100, y + 90), coach, fill="black", font=font)
#     draw.text((100, y + 140), phone, fill="black", font=font)

#     # Save image
#     filename = f"invite_{name.replace(' ', '_')}.jpg"
#     output_path = os.path.join(settings.MEDIA_ROOT, filename)
#     img.save(output_path)

#     invite_url = settings.MEDIA_URL + filename

#     Invite.objects.create(
#         customer_name=name,
#         customer_phone=customer_phone,
#         coach_name=coach,
#         coach_phone=phone,
#         event_date=date if date else None,
#         event_time=time if time else None,
#         image=filename
#     )


#     return JsonResponse({
#         "image": invite_url,
#         "whatsapp": whatsapp_link

#     })
