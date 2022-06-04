import React, {useEffect, useState} from 'react';
import {Col, Row} from 'antd';
import axios from "axios";
import MangaBlock from "../components/MangaBlock";


const Home = () => {

    const [manga, setManga] = useState([])

    const getManga = async () => {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': `JWT ${localStorage.getItem('access')}`
            }
        };
        const response = await axios.get(`http://localhost:8000/api/v1/archive/manga/`, config);

        setManga(response.data.results);
    };

    useEffect(() => {
        getManga();
    }, []);

    return (
        <div className="home">
            <h3 className="home-label">Популярная манга</h3>
            {manga && <MangaBlock manga={manga}/>}
        </div>
    );
};

export default Home;
