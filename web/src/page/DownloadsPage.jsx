import React, { useEffect, useState } from 'react'
import { Years, Months } from '../data/data'
import { Button, TextField, Switch, FormControlLabel } from "@material-ui/core";
import { makeStyles } from '@material-ui/styles'
import SimpleSelect from '../component/SimpleSelect';

const eel = window["eel"];

const useStyles = makeStyles({
  root: {
    padding: "12px 40px",
  },
  members: {
    display: 'flex',
    flexWrap: 'wrap',
    flexDirection: 'row',
    height: 120,
    overflowY: 'scroll',
    padding: '10px 20px 0 20px',
    border:'solid 1px #CCC',
    backgroundColor: '#EEEEEE80',
    position: 'relative',
    "&> div": {
      padding: 2,
      color:'#777',
      width:200,
      display: 'flex',
      // justifyContent: 'space-around',
      gap:12,
    }
  },
  membermsg: {
    color: '#777',
    textAlign: 'right',
    fontSize: '.85rem'
  }
})

const DownloadsPage = () => {
  const [message, setMessage] = useState({ text: "", type: 0 });
  const [users, setUsers] = useState([])
  const [val, setVal] = useState({
    Year: 2021,
    Month: '4',
    username: '',
    password: '',
    members: '',
    isSelf: true,
    async: false,
  });
  const cls = useStyles();

  useEffect(() => {
    setInitialFormData()
  }, [])

  /** 入力フォーム初期値 */
  const setInitialFormData = async () => {
    const response = await eel.getUsers()();
    const user_data = response.map(x=> ({...x, progress: 0})).filter(x=>x.status === '1')
    setUsers(user_data)
    console.log(user_data)
    const dt = new Date();
    const data = {
      Year: dt.getFullYear(),
      Month: String(dt.getMonth() + 1),
      username: '',
      password: '',
      members: user_data.map(x => x.id).join(","),
      isSelf: true,
      async: false,
    }
    setVal(data)
  }

  /** Form入力ハンドラー */
  const handleChange = (event) => {
    setVal({ ...val, [event.target.name]: event.target.value });
    // console.log(val);
  };

  /** 自身のデータを含めるのSwitch切り替え */
  const handleBool = (event) => {
    setVal({ ...val, [event.target.name]: event.target.checked });
  }

  // Pythonを呼び出して返り値受け取り...(2)
  async function handleSubmit() {
    console.log('Submit arg')
    console.log(val)
    let result = await eel.py_download_company(val)();
    console.log('Submit ret')
    console.log(result);
    // setVal(result)
  }

  /** アプリ終了(CloseでPython側でも終了関数実行) */
  const sys_exit = () => {
    window.close();
  }

  /** 前回データの読み込み(Python) */
  const pyLoadHistory = async () => {
    let result = await eel.load_pickle('company_cond')();
    result.members = val.members;
    setVal(result)
  }

  // THREAD: 618679 - ENTER
  // THREAD: 629600 - LOADED
  /** Update Message: Pythonから呼び出される */
  async function pyUpdateMessage(text_message) {
    const isErr = text_message.toUpperCase().includes('ERROR')
    console.log(isErr)
    let newUsers = [...users]
    if(text_message.slice(0,6) === 'THREAD'){
      const prog_idx = {'ENTER': 20,LOGIN:40, FIND:50, LOADED: 60, EXIT: 100}
      const user_id = text_message.slice(8, 14)
      const progress = prog_idx[text_message.split('-')[1].trim()]
      console.log(user_id, progress, newUsers.findIndex(x=>x.id===user_id))
      console.log(text_message)

      newUsers[newUsers.findIndex(x=>x.id===user_id)].progress = progress
      setUsers(newUsers)
    }
    setMessage({ text: text_message, type: isErr ? 9 : 0 })
  }
  try {
    window.eel.expose(pyUpdateMessage, 'pyUpdateMessage');
  } catch (err) {
    // console.error(err)
  }


  const styleDiv = {
    display: "flex", gap: 10, width: "80%", minWidth: 240, margin: 20,
    flexDirection: 'column',
  }

  return (
    <div style={styleDiv}>
      {/* Header */}
      <h3 style={{ display: "flex", justifyContent: "space-between" }}>
        <span>Company Data Organization</span>
        <Button onClick={pyLoadHistory} size="small" variant="outlined">
          load history
        </Button>
      </h3>

      {/* Information */}
      {message.text && message.type === 0 && (
        <div style={{ color: "gray", backgroundColor: "#EEF5FF", fontSize: "small", width: "80%", minWidth: 240, padding: 10, border: "1px solid #CCC" }}>
          {message.text}
        </div>
      )}
      {message.text && message.type === 9 && (
        <div style={{ color: "red", backgroundColor: "#FEC", fontSize: "small", width: "80%", minWidth: 240, padding: 10, border: "1px solid #CCC" }}>
          {message.text}
        </div>
      )}

      <br />
      {/* Login Form */}
      <div style={{ display: "flex", gap: 20, minWidth: 240 }}>
        <TextField
          style={{ width: "100%" }}
          label="username"
          name="username"
          placeholder="username"
          variant="standard"
          focused
          value={val["username"]}
          onChange={handleChange}
          helperText={"※ 社員番号"}
        />
        <TextField
          style={{ width: "100%" }}
          label="password"
          name="password"
          type="password"
          variant="standard"
          value={val["password"]}
          onChange={handleChange}
          focused
          helperText={""}
        />
      </div>

      {/* Year, Month */}
      <div style={{ display: "flex", gap: 20, minWidth: 240, marginTop: 20 }}>
        <SimpleSelect options={Years} name="Year" val={val} initialValue={2021} handleChange={handleChange} />
        <SimpleSelect options={Months} name="Month" val={val} initialValue={"04"} handleChange={handleChange} />
      </div>

      <br />
      <div>
        {/* 自身のデータを含める */}
        <FormControlLabel control={<Switch checked={val.isSelf} name="isSelf" onChange={handleBool} color="primary" />} label="自身のデータを含める" style={{ color: "#888" }} />
        {/* 非同期処理を有効にする */}
        <FormControlLabel control={<Switch checked={val.async} name="async" onChange={handleBool} color="primary" />} label="非同期処理を有効にする" style={{ color: "#888" }} />
      </div>

      {/* Members2 */}
      <div className={cls.members}>
        {users.map((user, index) => (
          <div key={`user-${user.id}`}>
            <span>{user.id}</span><span>{user.name}</span><span>{user.progress}%</span>
          </div>
        ))}
      </div>
      <span className={cls.membermsg}>※ 読み込みたいユーザー情報は「USER」タブから編集してください。</span>

      <div>
        <hr />
      </div>

      {/* Action Buttons */}
      <div style={{ display: "flex", gap: 10 }}>
        <Button onClick={handleSubmit} variant="contained" color="primary">
          send
        </Button>
        <Button onClick={sys_exit} variant="contained" color="secondary">
          cancel
        </Button>
      </div>
    </div>
  );
}



export default DownloadsPage