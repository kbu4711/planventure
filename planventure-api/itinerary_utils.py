"""
Utility functions for itinerary generation and management
"""
from datetime import datetime, timedelta, timezone, time
from models.itinerary_item import ItineraryItem


def generate_default_itinerary_template(trip_id, start_date, end_date, destination=""):
    """
    Generate a default itinerary template with placeholder items for each day of a trip.
    
    Args:
        trip_id (int): The ID of the trip
        start_date (datetime): The start date of the trip
        end_date (datetime): The end date of the trip
        destination (str, optional): The destination name for template customization
        
    Returns:
        list: List of dictionaries containing default itinerary item data ready for database insertion
        
    Example:
        >>> from datetime import datetime, timedelta
        >>> start = datetime(2026, 6, 1)
        >>> end = datetime(2026, 6, 5)
        >>> template = generate_default_itinerary_template(1, start, end, "Paris, France")
        >>> len(template)  # Returns 5 (days)
        5
    """
    template_items = []
    
    # Calculate the number of days in the trip
    current_date = start_date
    day_counter = 1
    
    while current_date.date() <= end_date.date():
        activity_date = current_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Generate default template for each day
        item_data = {
            'trip_id': trip_id,
            'day': day_counter,
            'title': f"Day {day_counter} - {destination}" if destination else f"Day {day_counter}",
            'description': f"Explore and discover {destination}" if destination else "Plan your activities for this day",
            'activity_date': activity_date,
            'location': destination if destination else None,
            'latitude': None,
            'longitude': None,
            'breakfast_time': time(8, 0),  # 8:00 AM
            'lunch_time': time(12, 0),     # 12:00 PM
            'dinner_time': time(19, 0),    # 7:00 PM
            'accommodation_name': None,
            'accommodation_address': None,
            'activities': [
                {
                    'name': 'Morning Activity',
                    'time': '09:00',
                    'duration_minutes': 120,
                    'location': destination if destination else 'Location TBD',
                    'notes': 'Add your morning activity here'
                },
                {
                    'name': 'Afternoon Activity',
                    'time': '14:00',
                    'duration_minutes': 120,
                    'location': destination if destination else 'Location TBD',
                    'notes': 'Add your afternoon activity here'
                }
            ]
        }
        
        template_items.append(item_data)
        
        # Move to next day
        current_date += timedelta(days=1)
        day_counter += 1
    
    return template_items


def generate_default_itinerary_objects(trip_id, start_date, end_date, destination=""):
    """
    Generate a default itinerary template as ItineraryItem model objects.
    
    Args:
        trip_id (int): The ID of the trip
        start_date (datetime): The start date of the trip
        end_date (datetime): The end date of the trip
        destination (str, optional): The destination name for template customization
        
    Returns:
        list: List of ItineraryItem model objects ready to be added to the database
        
    Example:
        >>> from datetime import datetime, timedelta
        >>> start = datetime(2026, 6, 1)
        >>> end = datetime(2026, 6, 5)
        >>> items = generate_default_itinerary_objects(1, start, end, "Paris, France")
        >>> all(isinstance(item, ItineraryItem) for item in items)
        True
    """
    itinerary_items = []
    template_data = generate_default_itinerary_template(trip_id, start_date, end_date, destination)
    
    for item_data in template_data:
        itinerary_item = ItineraryItem(
            trip_id=item_data['trip_id'],
            day=item_data['day'],
            title=item_data['title'],
            description=item_data['description'],
            activity_date=item_data['activity_date'],
            location=item_data['location'],
            latitude=item_data['latitude'],
            longitude=item_data['longitude'],
            breakfast_time=item_data['breakfast_time'],
            lunch_time=item_data['lunch_time'],
            dinner_time=item_data['dinner_time'],
            accommodation_name=item_data['accommodation_name'],
            accommodation_address=item_data['accommodation_address'],
            activities=item_data['activities']
        )
        itinerary_items.append(itinerary_item)
    
    return itinerary_items
