import { TextField, Checkbox, Button } from '@material-ui/core';
import React, { useState, useEffect } from 'react'
import { makeStyles } from '@material-ui/styles'
import { Delete } from '@material-ui/icons';
// import DeleteForeverIcon from '@mui/icons-material/DeleteForever';

// const eel = window["eel"];
const useStyles = makeStyles({
    root: {

    },
    message:{
        borderRadius:8,
        backgroundColor: "#EEEEEE80",
        padding:"8px 24px",
        width:"fit-content",
        color:"#888"
    },
    error: {
        borderRadius:8,
        padding:"8px 24px",
        width:"fit-content",
        backgroundColor: "#FFEEDD80",
        color:"red",
        whiteSpace: 'break-spaces'
    },
    userrow:{
        display: 'flex',
        gap: 20,
        alignItems: 'center'
    }
})

const Users = () => {

    const [users, setUsers] = useState([])
    const [errMsg, setErrMsg] = useState("")
    const cls = useStyles();

    /** データの読み込み(Python) */
    const getUsers = async () => {
        let result = await eel.getUsers()();
        setUsers(result)
        // console.log(result)
        if (result.map(x=>x.id).filter((x, i, self) => self.indexOf(x) !== i).length){
            setErrMsg("重複しているデータ(社員番号)があります。CSVデータを確認してください。\n" + result.map(x=>x.id).filter((x, i, self) => self.indexOf(x) !== i).join(","))
        } else {
            setErrMsg("")
        }
    }

    const openCsv = async () => {
        await eel.openUsersCsv()();
    }

    useEffect(() => {
        getUsers()
    }, [])
    

    const updateUser = async (orgData, payload) => {
        await eel.updateUser(orgData, payload)
        getUsers()
    }

    function handleSubmit(payload) {
        // console.log("handleSubmit")
        // console.log(payload)
        const newData = users;
        newData[payload.index][payload.key] = payload.value;
        // console.log(newData)
        // setUsers(newData)
        updateUser(users, payload)
    }


    const addUser = async() => {
        console.log("addUser")
        if (users.filter(x=>x.id==="").length === 0){
            await eel.addUser(users)();
            getUsers()
        } else {
            alert("不正なデータが存在するため処理が続行できません。\n空データを削除するなど修正をしてください。")
        }
    }

    const deleteUser = async(index) => {
        if(confirm("削除してもよろしいですか？")){
            // console.log('yes')
            await eel.deleteUser(users, index)();
            getUsers();
        }else{
            console.log('no!')
        }
    }

    return (
        <div className={cls.root}>
            <h1>Users</h1>
            {errMsg!=="" && <div className={cls.error}>{errMsg}</div>}
            <p className={cls.message}>テキスト入力欄は、編集後にEnterボタンを押すことで更新することができます。<br/>
            CSVを直接編集することも可能です。<a href="#" onClick={openCsv} style={{color:'blue', textDecoration:'underline'}}>CSVを開く</a></p>
            <br />
            <div className={cls.userrow} style={{marginBottom:10}}>
                <div style={{width:180}}>No</div>
                <div style={{width:180}}>Name</div>
                <div style={{width:45}}>Enable</div>
                <div style={{width:140}}>Created</div>
                <div style={{width:140}}>Modified</div>
            </div>
            {users.map((user, index) => (
                <div className={cls.userrow} key={index}>
                    <UserInputField index={index} name="id" value={user.id} handleSubmit={handleSubmit}/>
                    <UserInputField index={index} name="name" value={user.name} handleSubmit={handleSubmit}/>
                    <UserCheckBox index={index} checked={user.status} handleSubmit={handleSubmit}/>
                    <div style={{width:140}}>{user.created}</div>
                    <div style={{width:140}}>{user.modified}</div>
                    <Delete style={{color:'gray'}} onClick={()=>deleteUser(index)}></Delete>
                </div>
            ))}
            <br/>
            <Button onClick={addUser} color="primary" variant='contained'>ユーザー追加</Button>
        </div>
    )
}

const UserInputField = ({ index, name, value, handleSubmit }) => {
    const [userValue, setUserValue] = useState(value)
    function handleChange(e) {
        console.log("handleChange")
        console.log(e.target.value)
        setUserValue(e.target.value)
    }
    return (
        <TextField
            name={name}
            id={name + '-' + index}
            onChange={(e) => handleChange(e)}
            onKeyPress={(e) => {
                if (e.key === "Enter") {
                    handleSubmit({index:index, key:name, value:userValue});
                }
            }}
            title={value}
            value={userValue}
            InputLabelProps={{
                style: { color: "#AAF" },
            }}
            fullWidth={false}
            autoFocus={false}
            style={{ background: value === userValue ? "" : "yellow" }}
        />
    )
}

const UserCheckBox = ({index, checked, handleSubmit}) => {

    const [userChecked, setUserChecked] = useState(checked==='1'?true:false)

    function handleCheck(){
        setUserChecked(!userChecked)
        console.log(!userChecked, checked)
        handleSubmit({index:index, key:'status', value: userChecked? '1': '0'})
    }
    return (
        <Checkbox checked={userChecked} onChange={handleCheck}/>
    )

}

export default Users