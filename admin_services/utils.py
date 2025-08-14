from datetime import datetime, timedelta
from ai_engine.models import ChatMessage

def get_daily_message_counts(days: int):
    today = datetime.utcnow().date()
    end_datetime = datetime.combine(today, datetime.min.time())
    start_datetime = end_datetime - timedelta(days=days - 1)

    pipeline = [
        {
            "$match": {
                "deleted_at": None,
                "created_at": {
                    "$gte": start_datetime,
                    "$lt": end_datetime + timedelta(days=1)
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at"
                    }
                },
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "_id": 1 }  # Oldest to newest
        }
    ]

    results = ChatMessage.objects.aggregate(*pipeline)

    counts_map = {item["_id"]: item["count"] for item in results}

    # Build list from oldest to newest
    result = []
    for i in range(days):
        day = (start_datetime + timedelta(days=i)).date().isoformat()
        result.append({
            "date": day,
            "count": counts_map.get(day, 0)
        })

    return result
