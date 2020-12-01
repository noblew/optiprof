import React, { useState } from 'react'
import { 
    Form, 
    FormGroup, 
    Input, 
    InputGroupAddon, 
    InputGroup,
    Button
} from 'reactstrap'

const SearchBar = ({submitCallback, btnColor='primary'}) => {
    const [searchInput, setSearchInput] = useState("")

    const watchSearch = searchVal => {
        setSearchInput(searchVal)
    }
    
    const submitSearch = async (e) => {
        e.preventDefault()
        submitCallback(searchInput)
    }

    return (
        <Form onSubmit={submitSearch}>
            <FormGroup>
                <InputGroup>
                <Input placeholder="Search..." onChange={e => {watchSearch(e.target.value)}}/>
                <InputGroupAddon addonType="append">
                    <Button color={btnColor} type="submit">Search</Button>
                </InputGroupAddon>
                </InputGroup>
            </FormGroup>
        </Form>
    )
}

export default SearchBar 
