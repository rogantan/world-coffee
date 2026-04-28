// date_formatter.ts

// Вспомогательная функция для получения formatted parts
const getDateParts = (date: Date) => {
  const formatter = new Intl.DateTimeFormat('ru', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  const parts = formatter.formatToParts(date);
  
  const year = parts.find(part => part.type === 'year')?.value;
  const month = parts.find(part => part.type === 'month')?.value;
  const day = parts.find(part => part.type === 'day')?.value;
  
  if (!year || !month || !day) {
    throw new Error('Failed to format date');
  }
  
  return { year, month, day };
};

// Форматирование даты для начала дня
export const formatDateStart = (date: Date): string => {
  const { year, month, day } = getDateParts(date);
  return `${year}-${month}-${day}T00:00:00`;
}

// Форматирование даты для конца дня
export const formatEndDate = (date: Date): string => {  
  const { year, month, day } = getDateParts(date);
  return `${year}-${month}-${day} 23:59:00`;
}

// Форматирование только даты (без времени)
export const formatOnlyDate = (date: Date): string => {
  const { year, month, day } = getDateParts(date);
  return `${year}-${month}-${day}`;
}

// Получение постфикса в формате MM_YYYY
export const getDatePostfix = (date: Date): string => {
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  return `${month}_${year}`;
};