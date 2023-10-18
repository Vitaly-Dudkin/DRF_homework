import stripe

from courses.models import Course


def get_price_id(course_name, price):
    product = stripe.Product.create(
        name=course_name,
        description='The best course ever'
    )

    price_in_dollars = 100
    price = stripe.Price.create(
        unit_amount=price * price_in_dollars,
        currency="usd",
        product=product.id,
    )

    return price.id


def get_payment_link(pk_course):
    course = Course.objects.get(pk=pk_course)

    price_id = get_price_id(course.name, course.price)

    session = stripe.checkout.Session.create(
        success_url=f"http://127.0.0.1:8000/lesson/check_pay/{course.pk}",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
    )

    return session.url
