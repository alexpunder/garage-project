import io

from django.http import FileResponse
from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.platypus.flowables import Flowable

from autoweb.settings import BASE_DIR
from .utils import wrap_row
from .services import OrderServices


class CustomLine(Flowable):
    def __init__(self, width, color):
        Flowable.__init__(self)
        self.width = width
        self.color = color

    def wrap(self, *args, **kwargs):
        return self.width, 1

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(1)
        self.canv.line(0, 0, self.width, 0)


pdfmetrics.registerFont(
    TTFont('DejaVuSans', BASE_DIR / 'static/fonts/DejaVuSans.ttf')
)
pdfmetrics.registerFont(
    TTFont(
        'DejaVuSans-Bold', BASE_DIR / 'static/fonts/DejaVuSans-Bold.ttf'
    )

)


def order_pdf_file(request, pk):
    buffer = io.BytesIO()

    # Данные для формирования квитанции
    user = request.user
    order, order_items = OrderServices.get_order_and_items(
        user, pk
    )

    # Инициализация PDF-документа
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        title=f'Order #{order.id}',
        topMargin=20, bottomMargin=20,
        leftMargin=36, rightMargin=36,
    )

    # Стили
    styles = getSampleStyleSheet()
    header_info_style = styles['Title']
    header_info_style.fontName = 'DejaVuSans'
    header_info_style.alignment = TA_LEFT
    trader_header_style = styles['Heading4']
    trader_header_style.fontName = 'DejaVuSans-Bold'
    trader_header_style.alignment = TA_LEFT
    trader_text_style = styles['Italic']
    trader_text_style.fontName = 'DejaVuSans'
    trader_text_style.alignment = TA_LEFT
    customer_header_style = styles['Heading4']
    customer_header_style.fontName = 'DejaVuSans-Bold'
    customer_header_style.alignment = TA_LEFT
    customer_text_style = styles['Italic']
    customer_text_style.fontName = 'DejaVuSans'
    customer_text_style.alignment = TA_LEFT
    total_order_inf_style = styles['Italic']
    total_order_inf_style.fontName = 'DejaVuSans'
    total_order_inf_style.alignment = TA_LEFT
    total_order_text_style = styles['Heading4']
    total_order_text_style.fontName = 'DejaVuSans-Bold'
    total_order_text_style.alignment = TA_LEFT

    # Заголовок заказа
    created_at = order.created_at.strftime('%d.%m.%Y')
    header_text = f'Квитанция к заказу клиента № {order.id} от {created_at}'
    header_parag = Paragraph(header_text, header_info_style)

    # Информация о продавце
    trader_header = 'Исполнитель:'
    trader_text = (
        'ИП Литвинов Р.С., ИНН 342800105419, '
        'Волгоградская обл., Волжский, ул. Пушкина 51д/317;<br/>тел.: '
        '8 (927) 066-99-00'
    )

    trader_header_parag = Paragraph(trader_header, trader_header_style)
    trader_text_parag = Paragraph(trader_text, trader_text_style)
    trader_info_block = KeepTogether(
        [trader_header_parag, trader_text_parag]
    )

    # Информация о заказчике
    customer_header = 'Заказчик:'
    customer_text = (
        f'{user.first_name} {user.last_name}<br/>тел.: {user.phone_number}'
    )

    customer_header_parag = Paragraph(customer_header, customer_header_style)
    customer_text_parag = Paragraph(customer_text, customer_text_style)
    customer_info_block = KeepTogether(
        [customer_header_parag, customer_text_parag]
    )

    # Информация с количеством товаров и общей стоимостью, num2words
    total_price = num2words(
        order.total_price, lang='ru', to='currency', currency='RUB'
    ).capitalize()
    total_order_inf = (
        f'Всего наименований {order.count}, на сумму {order.total_price} руб.'
    )
    total_order_text = f'{total_price}'

    total_order_inf_parag = Paragraph(
        total_order_inf, total_order_inf_style
    )
    total_order_text_parag = Paragraph(
        total_order_text, total_order_text_style
    )
    total_order_info_block = KeepTogether(
        [total_order_inf_parag, total_order_text_parag]
    )

    # Отступы
    spacer = Spacer(1, 12)
    small_spacer = Spacer(1, 6)

    # Основная таблица для товаров в заказе
    data = [
        ['Код', 'Производитель', 'Наименование',
         'Кол-во', 'Цена, руб.', 'Сумма, руб.']
    ]

    for order_item in order_items:
        cut_title = wrap_row(order_item.product.title, 20)
        data.append([
            order_item.product.article,
            order_item.product.brand,
            cut_title,
            order_item.quantity,
            order_item.price_at_time_of_order,
            order_item.total_price
        ])
    data.append(['', '', '', '', 'Итого:', f'{order.total_price}'])

    col_widths = [70, 110, 140, 50, 85, 85]

    # Стиль таблицы
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('TOPPADDING', (0, 0), (-1, 0), 2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),

        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),

        ('GRID', (0, 0), (-1, -2), 1, colors.black),

        ('BOX', (-2, -1), (-1, -1), 1, colors.black),
        ('INNER_GRID', (4, -1), (-1, -1), 1, colors.black),
    ]))

    rightMargin = 72
    drow_simple_line = CustomLine(
        width=(A4[0] - rightMargin), color=colors.black
    )

    doc.build(
        [header_parag, small_spacer, trader_info_block, customer_info_block,
         spacer, table, small_spacer, total_order_info_block, spacer,
         drow_simple_line]
    )
    buffer.seek(0)

    return FileResponse(
        buffer, as_attachment=True, filename=f"Order_{order.id}.pdf"
    )
