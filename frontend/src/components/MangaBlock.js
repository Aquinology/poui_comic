import React from 'react';
import {Card, Col, Row} from "antd";

const { Meta } = Card;

const MangaBlock = ({manga}) => {
    return (
        <Row gutter={[16, 24]}>
            {manga.map(item => (
                <Col className="gutter-row" span={6}>
                    <Card key={item.title} className="home-manga-list" cover={
                        <img alt={item.title} src={item.manga_pic} />
                    }>
                        <h5 className="witeeee">{item.title}</h5>
                    </Card>
                </Col>
                )
            )}
        </Row>
    );
};

export default MangaBlock;