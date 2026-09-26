import pymupdf
import os

pdf_path = r'C:\Users\FERO_ADM\.gemini\antigravity\brain\804d2162-904e-4d53-a4d6-31fe80de76a4\.user_uploaded\media_1790419508390.pdf'
out_dir = r'C:\Users\FERO_ADM\.gemini\antigravity\scratch\quantux-v4-dev\docs_mock_images'
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)

mock_names = {
    (11, 0): 'figura_1_portal_centrado.png',
    (12, 0): 'figura_2_chat_stream.png',
    (12, 1): 'figura_3_modal_crear_solicitud.png',
    (13, 0): 'figura_4_historial_mis_solicitudes.png',
    (13, 1): 'figura_5_detalle_n2_mim.png',
    (14, 0): 'figura_6_mando_lider_rescate.png',
    (14, 1): 'figura_7_configuracion_itil_slas.png',
}

extracted = []
for page_num in [11, 12, 13, 14]:
    page = doc[page_num - 1]
    image_list = page.get_images(full=True)
    print(f"Page {page_num}: {len(image_list)} images")
    for img_idx, img_info in enumerate(image_list):
        xref = img_info[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image['image']
        image_ext = base_image['ext']
        w = base_image['width']
        h = base_image['height']
        fname = mock_names.get((page_num, img_idx), f"page_{page_num}_img_{img_idx}.{image_ext}")
        out_path = os.path.join(out_dir, fname)
        with open(out_path, 'wb') as f:
            f.write(image_bytes)
        print(f"  Extracted {fname}: {w}x{h} ({image_ext})")
        extracted.append(out_path)

print(f"Successfully extracted {len(extracted)} mock images to {out_dir}")
