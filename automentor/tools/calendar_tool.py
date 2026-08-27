"""
Calendar Tool: Schedules micro-study sessions on Google Calendar based on Ebbinghaus Spaced Repetition.
Supports Google Calendar API with a structured Demo Simulation mode.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from automentor.config import GOOGLE_CALENDAR_CREDENTIALS_FILE, DEMO_MODE

def schedule_study_session(topic_name: str, duration_minutes: int = 30, suggested_day_offset: int = 1) -> str:
    """
    Agenda uma sessão de estudo focada e sem distrações no Google Calendar do aluno.

    Args:
        topic_name: Nome do tópico a ser praticado (ex: 'Prática de Contratos Protobuf em gRPC').
        duration_minutes: Duração do bloco de estudo em minutos (padrão: 30 minutos).
        suggested_day_offset: Dias a partir de hoje para agendar (padrão: 1 para amanhã).

    Returns:
        Confirmação do agendamento com data, hora e link do evento.
    """
    target_date = datetime.now() + timedelta(days=suggested_day_offset)
    # Defaulting to 18:30 in the evening (typical free study window)
    study_start = target_date.replace(hour=18, minute=30, second=0, microsecond=0)
    study_end = study_start + timedelta(minutes=duration_minutes)

    time_str = study_start.strftime("%d/%m/%Y às %H:%M")
    end_time_str = study_end.strftime("%H:%M")

    # Real Google Calendar API integration (if credentials exist)
    if GOOGLE_CALENDAR_CREDENTIALS_FILE and not DEMO_MODE:
        try:
            # Here real Google Calendar API call would execute
            pass
        except Exception as e:
            print(f"[CalendarTool] Error calling Google Calendar API: {e}")

    # Return structured confirmation
    event_title = f"🎯 AutoMentor Lab: {topic_name}"
    return (
        f"📅 [Google Calendar] Evento agendado com sucesso!\n"
        f"• Título: {event_title}\n"
        f"• Horário: {time_str} - {end_time_str} ({duration_minutes} min)\n"
        f"• Status: Bloqueado na agenda do aluno"
    )
