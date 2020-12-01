import React, { useState } from 'react'
import { 
    LineChart, 
    CartesianGrid, 
    XAxis, 
    YAxis, 
    Tooltip, 
    Legend, 
    Line 
} from 'recharts'

const GPAChart = ({ gpaData }) => {
    return (
        <LineChart>
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
        </LineChart>
    )
}