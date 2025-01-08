import React from 'react';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { useLanguage } from '../../contexts/LanguageContext';

const LanguageSelector: React.FC = () => {
    const { language, setLanguage } = useLanguage();

    return (
        <FormControl sx={{ m: 1, minWidth: 120 }}>
            <InputLabel>Language</InputLabel>
            <Select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                label="Language"
            >
                <MenuItem value="en-US">English (US)</MenuItem>
                <MenuItem value="en-UK">English (UK)</MenuItem>
                <MenuItem value="en-IN">English (India)</MenuItem>
                <MenuItem value="de">German</MenuItem>
            </Select>
        </FormControl>
    );
};

export default LanguageSelector;