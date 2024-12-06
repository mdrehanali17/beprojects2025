import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const CustomDatePicker = ({ selectedDate, onChange }) => {
  // Date constraints
  const today = new Date();
  const maxDate = new Date();
  maxDate.setDate(today.getDate() + 2); 

  return (
    <DatePicker
      selected={selectedDate}
      onChange={onChange}
      minDate={today}
      maxDate={maxDate}
      placeholderText="DD/MM/YYYY"
      dateFormat="dd/MM/yyyy"
      className="form-control"
    />
  );
};

export default CustomDatePicker;
