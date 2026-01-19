"""Statistics response models."""

from pydantic import BaseModel, computed_field


def grosze_to_pln(grosze: int) -> float:
    """Konwertuj grosze na PLN."""
    return grosze / 100


class BasicStats(BaseModel):
    """Basic statistics response model."""

    fiscal_total: int  # grosze
    total_with_packs: int  # grosze
    total_discount: int  # grosze
    receipts_count: int
    items_count: int

    @computed_field
    @property
    def fiscal_total_pln(self) -> float:
        """Fiscal total in PLN."""
        return grosze_to_pln(self.fiscal_total)

    @computed_field
    @property
    def total_with_packs_pln(self) -> float:
        """Total with packs in PLN."""
        return grosze_to_pln(self.total_with_packs)

    @computed_field
    @property
    def total_discount_pln(self) -> float:
        """Total discount in PLN."""
        return grosze_to_pln(self.total_discount)

    @computed_field
    @property
    def discount_percent(self) -> float:
        """Discount percentage of total spending."""
        if self.fiscal_total == 0:
            return 0.0
        return round((self.total_discount / self.fiscal_total) * 100, 2)

    @computed_field
    @property
    def avg_receipt_value_pln(self) -> float:
        """Average receipt value in PLN."""
        if self.receipts_count == 0:
            return 0.0
        return round(grosze_to_pln(self.fiscal_total) / self.receipts_count, 2)


class TopProduct(BaseModel):
    """Top product model for statistics."""

    name: str
    count: int  # liczba zakupów
    total_quantity: float  # suma ilości
    total_spent: int  # grosze

    @computed_field
    @property
    def total_spent_pln(self) -> float:
        """Total spent in PLN."""
        return grosze_to_pln(self.total_spent)


class TimeDistributionDay(BaseModel):
    """Time distribution by day of week."""

    monday: int = 0
    tuesday: int = 0
    wednesday: int = 0
    thursday: int = 0
    friday: int = 0
    saturday: int = 0
    sunday: int = 0

    def to_dict(self) -> dict[str, int]:
        """Convert to dictionary."""
        return {
            "Monday": self.monday,
            "Tuesday": self.tuesday,
            "Wednesday": self.wednesday,
            "Thursday": self.thursday,
            "Friday": self.friday,
            "Saturday": self.saturday,
            "Sunday": self.sunday,
        }


class TimeDistribution(BaseModel):
    """Time distribution statistics."""

    day_of_week: dict[str, int]  # {"Monday": 5, "Tuesday": 3, ...}
    hour: dict[int, int]  # {8: 3, 12: 5, 18: 7, ...}

    @computed_field
    @property
    def favorite_day(self) -> str | None:
        """Most frequent shopping day."""
        if not self.day_of_week:
            return None
        return max(self.day_of_week, key=self.day_of_week.get)

    @computed_field
    @property
    def favorite_hour(self) -> int | None:
        """Most frequent shopping hour."""
        if not self.hour:
            return None
        return max(self.hour, key=self.hour.get)


class MonthlySpending(BaseModel):
    """Monthly spending statistics."""

    year: int
    month: int
    fiscal_total: int  # grosze
    receipts_count: int

    @computed_field
    @property
    def fiscal_total_pln(self) -> float:
        """Fiscal total in PLN."""
        return grosze_to_pln(self.fiscal_total)


class StoreStats(BaseModel):
    """Store-level statistics."""

    store_number: str
    receipts_count: int
    total_spent: int  # grosze

    @computed_field
    @property
    def total_spent_pln(self) -> float:
        """Total spent in PLN."""
        return grosze_to_pln(self.total_spent)


class FunFact(BaseModel):
    """Fun fact for Wrapped feature."""

    fact_type: str  # np. "most_expensive_item", "earliest_shopping", etc.
    title: str
    value: str
    emoji: str = ""


class WrappedData(BaseModel):
    """Wrapped summary response model."""

    period: str  # "2024" lub "2024-01"
    top_products: list[TopProduct]
    total_spent_pln: float
    total_saved_pln: float
    favorite_day: str | None
    favorite_hour: int | None
    receipts_count: int
    items_count: int
    unique_products_count: int
    fun_facts: list[FunFact] = []

    @computed_field
    @property
    def savings_percent(self) -> float:
        """Savings percentage."""
        if self.total_spent_pln == 0:
            return 0.0
        return round((self.total_saved_pln / self.total_spent_pln) * 100, 2)


class CategoryStats(BaseModel):
    """Category-level statistics (for future AI categorization)."""

    category_name: str
    items_count: int
    total_spent: int  # grosze

    @computed_field
    @property
    def total_spent_pln(self) -> float:
        """Total spent in PLN."""
        return grosze_to_pln(self.total_spent)


class DashboardStats(BaseModel):
    """Complete dashboard statistics response."""

    basic: BasicStats
    top_products: list[TopProduct]
    time_distribution: TimeDistribution
    monthly_spending: list[MonthlySpending]
