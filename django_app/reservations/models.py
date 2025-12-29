import uuid
from django.db import models
from django.conf import settings

class Reservation(models.Model):
    """
    [공통 예약 테이블] (reservations)
    - 항공, 기차, 숙소 등 모든 예약의 공통 정보를 담습니다.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="예약 ID")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations', db_column='user_id')
    
    class ReservationType(models.TextChoices):
        FLIGHT = 'FLIGHT', 'Flight'
        TRAIN = 'TRAIN', 'Train' # 나중에 추가될 수 있음
        SUBWAY = 'SUBWAY', 'Subway'
        
    type = models.CharField(max_length=10, choices=ReservationType.choices, default=ReservationType.FLIGHT)
    
    class ReservationStatus(models.TextChoices):
        CONFIRMED_TEST = 'CONFIRMED_TEST', 'Confirmed (Test)' # 결제 성공 시
        PENDING = 'PENDING', 'Pending'
        CANCELLED = 'CANCELLED', 'Cancelled'
        FAILED = 'FAILED', 'Failed'
        
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    title = models.CharField(max_length=200, help_text="예약 제목 (예: GMP -> CJU)")
    
    # 일정 및 금액
    start_at = models.DateTimeField(help_text="여행 시작 일시")
    end_at = models.DateTimeField(null=True, blank=True, help_text="여행 종료 일시")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="총 결제 금액")
    currency = models.CharField(max_length=3, default='KRW', help_text="통화")
    
    # 제공사 및 테스트 정보
    provider = models.CharField(max_length=50, null=True, blank=True, help_text="항공 데이터 제공사")
    provider_ref = models.CharField(max_length=120, null=True, blank=True, help_text="제공사 Flight/Offer ID")
    test_order_no = models.CharField(max_length=80, help_text="UI 노출용 테스트 주문번호")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservations'
        ordering = ['-created_at']

class ReservationFlight(models.Model):
    """
    [항공 예약 상세] (reservation_flights)
    - Reservation 테이블과 1:1 관계 (확장)
    """
    # 부모 예약 ID를 PK로 사용 (OneToOne)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, primary_key=True, related_name='flight_detail')
    
    class TripType(models.TextChoices):
        ONEWAY = 'ONEWAY', 'One Way'
        ROUNDTRIP = 'ROUNDTRIP', 'Round Trip'
        
    trip_type = models.CharField(max_length=10, choices=TripType.choices)
    cabin_class = models.CharField(max_length=30, help_text="좌석 등급")
    
    # 인원 수
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)
    
    # 부가 정보 (텍스트)
    baggage_info = models.TextField(null=True, blank=True, help_text="수하물 정보")
    refund_rule = models.TextField(null=True, blank=True, help_text="환불/변경 규정")
    special_request = models.TextField(null=True, blank=True, help_text="특별 요청사항")
    
    # 연락처
    contact_email = models.CharField(max_length=120, null=True, blank=True)
    contact_phone = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'reservation_flights'

class ReservationFlightSegment(models.Model):
    """
    [항공 구간 정보] (reservation_flight_segments)
    - 왕복인 경우 가는편/오는편, 경유가 있는 경우 여러 구간이 생김
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='segments')
    
    class Direction(models.TextChoices):
        OUTBOUND = 'OUTBOUND', 'Outbound'
        INBOUND = 'INBOUND', 'Inbound'
        
    direction = models.CharField(max_length=10, choices=Direction.choices)
    segment_no = models.IntegerField(help_text="구간 순서")
    
    airline_code = models.CharField(max_length=10, null=True, blank=True)
    flight_no = models.CharField(max_length=20, null=True, blank=True)
    
    dep_airport = models.CharField(max_length=10, help_text="출발 공항 코드")
    arr_airport = models.CharField(max_length=10, help_text="도착 공항 코드")
    
    dep_at = models.DateTimeField(help_text="출발 시각")
    arr_at = models.DateTimeField(help_text="도착 시각")
    
    duration_min = models.IntegerField(null=True, blank=True, help_text="소요 시간(분)")
    fare_per_person = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="1인 기준 요금")
    seat_availability_note = models.CharField(max_length=80, null=True, blank=True, help_text="잔여 좌석 정보")

    class Meta:
        db_table = 'reservation_flight_segments'
        ordering = ['direction', 'segment_no']

class ReservationPassenger(models.Model):
    """
    [승객 정보] (reservation_passengers)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='passengers')
    
    class PassengerType(models.TextChoices):
        ADT = 'ADT', 'Adult'
        CHD = 'CHD', 'Child'
        INF = 'INF', 'Infant'
        
    passenger_type = models.CharField(max_length=10, choices=PassengerType.choices)
    full_name = models.CharField(max_length=100, help_text="승객 이름")
    birth_date = models.DateField(null=True, blank=True)
    passport_no = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'reservation_passengers'

class ReservationSeatSelection(models.Model):
    """
    [좌석 선택 - 테스트용] (reservation_seat_selections)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='seat_selections')
    passenger = models.ForeignKey(ReservationPassenger, on_delete=models.SET_NULL, null=True, blank=True, related_name='seats')
    
    direction = models.CharField(max_length=10, choices=[('OUTBOUND', 'Outbound'), ('INBOUND', 'Inbound')])
    segment_no = models.IntegerField()
    
    seat_no = models.CharField(max_length=10, null=True, blank=True, help_text="좌석 번호 (예: 12A)")
    seat_note = models.TextField(null=True, blank=True, help_text="테스트 저장용 메모")

    class Meta:
        db_table = 'reservation_seat_selections'

class PaymentTransaction(models.Model):
    """
    [결제 트랜잭션 - 토스] (payment_transactions)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 예약 생성 전 결제 시도 단계에서는 reservation이 null일 수 있음
    reservation = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    
    provider = models.CharField(max_length=30, default='TOSS_PAYMENTS')
    
    class PaymentStatus(models.TextChoices):
        READY = 'READY', 'Ready'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.READY)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KRW')
    
    order_id = models.CharField(max_length=80, help_text="주문 ID")
    payment_key = models.CharField(max_length=120, null=True, blank=True, help_text="토스 PaymentKey")
    
    # 실패 사유 기록
    fail_code = models.CharField(max_length=80, null=True, blank=True)
    fail_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_transactions'