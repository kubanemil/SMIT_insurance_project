

async def group_tariff_by_date(tariff):
    grouped_data = {}
    async for item in tariff:
        date = item.date.isoformat()
        cargo_type_names = await item.cargo_type.values_list('name', flat=True)
        type_rate = {
            'cargo_type': cargo_type_names,
            'rate': item.rate
        }
        if date not in grouped_data:
            grouped_data[date] = []
        grouped_data[date].append(type_rate)
    return grouped_data
