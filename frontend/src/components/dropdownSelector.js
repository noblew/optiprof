import React, { useState } from 'react'
import {
    Dropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem
} from 'reactstrap'

const DropdownSelector = ({ optionsList, defaultText, selectCallback }) => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [active, setActive] = useState(defaultText)

    const dropdownToggle = () => {
        setDropdownOpen(prevState => !prevState)
    }

    const updateActive = (selectedVal) => {
        setActive(selectedVal)
        selectCallback(selectedVal)
    }

    return (
        <Dropdown isOpen={dropdownOpen} toggle={dropdownToggle}>
            <DropdownToggle caret>
                {active.charAt(0).toUpperCase() + active.slice(1)}
            </DropdownToggle>
            <DropdownMenu>
                {optionsList.map((val, idx) => {
                    return <DropdownItem key={idx} onClick={e => {updateActive(e.target.value)}} value={val}>
                        {val.charAt(0).toUpperCase() + val.slice(1)}
                    </DropdownItem>
                })}
            </DropdownMenu>
        </Dropdown>
    )
}

export default DropdownSelector