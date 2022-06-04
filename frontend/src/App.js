import React, {useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'antd/dist/antd.css';
import './App.css';
import {
    BellOutlined,
    UserOutlined,
    HomeOutlined,
    SearchOutlined,
    ImportOutlined,
    IdcardOutlined,
    SettingOutlined,
    EditOutlined,
    UserAddOutlined,
    UsergroupAddOutlined,
    FormOutlined,
    TeamOutlined,
    InboxOutlined
} from '@ant-design/icons';
import {BrowserRouter, Routes, Route} from "react-router-dom";
import {connect} from "react-redux";
import {Link} from 'react-router-dom';
import {checkAuthenticated, logout} from "./actions/authActions";
import {Layout, Menu, Dropdown} from 'antd';
import Home from "./containers/Home";
import Login from "./containers/Login";
import Register from "./containers/Register";
import Profile from "./containers/Profile";
import NotFound from "./containers/NotFound";
import Activate from "./containers/Activate";
import ResetPassword from "./containers/ResetPassword";
import ResetPasswordConfirm from "./containers/ResetPasswordConfirm";
import Settings from "./containers/Settings";
import Team from "./containers/Team";
import TeamAdd from "./containers/TeamAdd";
import TeamUpdate from "./containers/TeamUpdate";
import Teams from "./containers/Teams";
import Notifications from "./containers/Notifications";
import ModerRequests from "./containers/ModerRequests";
import MangaUpdate from "./containers/MangaUpdate";
import MangaAdd from "./containers/MangaAdd";
import Manga from "./containers/Manga";
import ChapterUpdate from "./containers/ChapterUpdate";
import ChapterAdd from "./containers/ChapterAdd";
import Chapter from "./containers/Chapter";
import Catalog from "./containers/Catalog";
import AuthorUpdate from "./containers/AuthorUpdate";
import AuthorAdd from "./containers/AuthorAdd";
import Author from "./containers/Author";
import Additions from "./containers/Additions";

const { Header, Footer, Content } = Layout;

function App({checkAuthenticated, logout, isAuthenticated}) {

    useEffect(() => {
        checkAuthenticated();
    }, []);

    const signout = () => {
        console.log('Logout')
        logout();
    };

    const guestLinks = () => (
        <>
            <Menu.Item className="sector-right" key="signin">
                <Link className="navigation-link" to="/signin">
                    Вход
                </Link>
            </Menu.Item>
            <Menu.Item key="signup">
                <Link className="navigation-link" to="/signup">
                    <div className="signup"><span>Регистрация</span></div>
                </Link>
            </Menu.Item>
        </>
    );

    const authLinks = () => (
        <>
            <Menu.Item className="sector-right" key="any-create">
                <Dropdown overlay={
                    <Menu className="navigation-dropdown" theme="dark">
                        <Menu.Item key="manga-create">
                            <Link className="navigation-link" key="manga-add" to="/manga/create">
                                <FormOutlined className="link-icon"/>Добавить тайтл
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="author-create">
                            <Link className="navigation-link" key="author-add" to="/author/create">
                                <UserAddOutlined className="link-icon"/>Добавить автора
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="team-create">
                            <Link className="navigation-link" key="team-add" to="/team/create">
                                <UsergroupAddOutlined className="link-icon"/>Добавить команду
                            </Link>
                        </Menu.Item>
                    </Menu>
                } placement="bottomRight" arrow>
                    <EditOutlined className="navigation-icon"/>
                </Dropdown>
            </Menu.Item>
            <Menu.Item key="notice">
                <Link className="navigation-link" to="/notifications">
                    <BellOutlined className="navigation-icon"/>
                </Link>
            </Menu.Item>
            <Menu.Item key="avatar">
                <Dropdown overlay={
                    <Menu className="navigation-dropdown" theme="dark">
                        <Menu.Item key="profile">
                            <Link className="navigation-link" key="profile" to="/profile">
                                <IdcardOutlined className="link-icon"/>Профиль
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="notifications">
                            <Link className="navigation-link" key="notifications" to="/notifications">
                                <BellOutlined className="link-icon"/>Уведомления
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="team">
                            <Link className="navigation-link" key="teams" to="/teams">
                                <TeamOutlined className="link-icon"/>Мои команды
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="additions">
                            <Link className="navigation-link" key="groups" to="/additions">
                                <InboxOutlined className="link-icon"/>Мои добавления
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="settings">
                            <Link className="navigation-link" key="settings" to="/settings">
                                <SettingOutlined className="link-icon"/>Настройки
                            </Link>
                        </Menu.Item>
                        <Menu.Item key="logout">
                            <Link className="navigation-link" key="logout" to="/" onClick={signout}>
                                <ImportOutlined className="link-icon"/>Выход
                            </Link>
                        </Menu.Item>
                    </Menu>
                } placement="bottomRight" arrow>
                    <UserOutlined className="avatar"/>
                </Dropdown>
            </Menu.Item>
        </>
    );

    return (
        <BrowserRouter>
            <Layout className="site-layout">
                <Header className="site-header">
                    <div className="logo">AquiRead</div>
                    <div className="main-menu">
                        <Menu className="navigation-sector" theme="dark" mode="horizontal">
                            <Menu.Item key="home">
                                <Link className="navigation-link" to="/">
                                    <HomeOutlined className="navigation-icon"/>
                                </Link>
                            </Menu.Item>
                            <Menu.Item key="catalog">
                                <Link className="navigation-link" to="/catalog">
                                    <SearchOutlined className="navigation-icon"/>
                                </Link>
                            </Menu.Item>
                            {isAuthenticated ? authLinks() : guestLinks()}
                        </Menu>
                    </div>
                </Header>
                <Content className="site-content">
                    <Routes>
                        <Route exact path='/' element={ <Home /> } />
                        <Route exact path='/signin' element={ <Login /> } />
                        <Route exact path='/signup' element={ <Register /> } />
                        <Route exact path='/profile' element={ <Profile /> } />
                        <Route exact path='/activate/:uid/:token' element={ <Activate /> } />
                        <Route exact path='/reset-password' element={ <ResetPassword /> } />
                        <Route exact path='/reset-password/confirm/:uid/:token' element={ <ResetPasswordConfirm /> } />
                        <Route exact path='/catalog' element={ <Catalog /> } />
                        <Route exact path='/settings' element={ <Settings /> } />
                        <Route exact path='/notifications' element={ <Notifications /> } />
                        <Route exact path='/additions' element={ <Additions /> } />
                        <Route exact path='/author' element={ <Author /> } />
                        <Route exact path='/author/create' element={ <AuthorAdd /> } />
                        <Route exact path='/author/update' element={ <AuthorUpdate /> } />
                        <Route exact path='/chapter' element={ <Chapter /> } />
                        <Route exact path='/chapter/create' element={ <ChapterAdd /> } />
                        <Route exact path='/chapter/update' element={ <ChapterUpdate /> } />
                        <Route exact path='/manga' element={ <Manga /> } />
                        <Route exact path='/manga/create' element={ <MangaAdd /> } />
                        <Route exact path='/manga/update' element={ <MangaUpdate /> } />
                        <Route exact path='/moder-requests' element={ <ModerRequests /> } />
                        <Route exact path='/team' element={ <Team /> } />
                        <Route exact path='/teams' element={ <Teams /> } />
                        <Route exact path='/team/create' element={ <TeamAdd /> } />
                        <Route exact path='/team/update' element={ <TeamUpdate /> } />
                        <Route exact path='*' element={ <NotFound /> } />
                    </Routes>
                </Content>
                <Footer className="site-footer">
                    AquiRead ©2022 Created by Aquinology
                </Footer>
            </Layout>
        </BrowserRouter>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.authReducer.isAuthenticated
});

export default connect(mapStateToProps, {checkAuthenticated, logout})(App);
