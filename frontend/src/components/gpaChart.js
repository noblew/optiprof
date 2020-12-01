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

import {
    Row,
    Col
} from 'reactstrap'

const GPAChart = ({ gpaData, criteria }) => {
    if (criteria === 'professor') {
        return (
            <LineChart>
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
            </LineChart>
        )
    } else {
        
    }
}