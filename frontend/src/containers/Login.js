import React, {useState} from 'react';
import {connect} from 'react-redux';
import {Link, Navigate} from 'react-router-dom';
import {Form, Button, Container, Row, Col} from 'react-bootstrap';
import {login} from '../actions/authActions';


const Login = ({login, isAuthenticated}) => {

    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const {username, password} = formData;

    function handleChange(event) {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    }

    function handleSubmit(event) {
        event.preventDefault();
        console.log('Login')
        login(username, password);
    }

    if (isAuthenticated) {
        return <Navigate to='/' />
    }

    return (
        <Container>
            <Row>
                <Col md={{ span: 6, offset: 3 }} className="witeeee">
                    <h1 className='mainTitle'>Sign in</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" name="username" placeholder="Enter your username"
                                          value={username} onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" name="password" placeholder="Enter your password"
                                          value={password} onChange={handleChange}/>
                        </Form.Group>
                        <Button variant="dark" type="submit">
                            Submit
                        </Button>
                    </Form>
                    <br/>
                    <div className='formLink'>
                        <p>Don't have an account?</p>
                        <Link to='/signup'>Sign up</Link>
                    </div>
                    <div className='formLink'>
                        <p>Forgot your password?</p>
                        <Link to='/reset-password'>Reset password</Link>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.authReducer.isAuthenticated
});

export default connect(mapStateToProps, {login})(Login);
