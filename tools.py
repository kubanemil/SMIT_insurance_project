

async def group_tariff_by_date(tariff):
    grouped_data = {}
    async for item in tariff:
        date = item.date.isoformat()
        type_rate = {
            'cargo_type': item.cargo_type,
            'rate': item.rate
        }
        if date not in grouped_data:
            grouped_data[date] = []
        grouped_data[date].append(type_rate)
    return grouped_data
