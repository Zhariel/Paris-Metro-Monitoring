import React from "react";
import "./button.css"

export const Button = ({
    children,
    type,
    onClick,
    buttonStyle,
    buttonSize
}) => {
    return(
        <button onClick={onClick} type={type} className='btn'>
            {children}
        </button>
    )
}