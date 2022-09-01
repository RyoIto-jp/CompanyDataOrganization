import React from 'react'
import { Years, Months } from '../data/data'
import { Button, TextField, Switch, FormControlLabel } from "@material-ui/core";
import SimpleSelect from '../component/SimpleSelect';

const eel = window["eel"];

const DownloadsPage = () => {
  const [message, setMessage] = React.useState({ text: "", type: 0 });
  const [val, setVal] = React.useState({
    Year: 2021,
    Month: '4',
    username: '',
    password: '',
    members: '',
    isSelf: true
  });

  const handleChange = (event) => {
    setVal({ ...val, [event.target.name]: event.target.value });
    console.log(val);
  };

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
    setVal(result)
  }

  /** Update Message: Pythonから呼び出される */
  function pyUpdateMessage(text_message) {
    const isErr = text_message.toUpperCase().includes('ERROR')
    console.log(isErr)
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
      {/* User Data */}
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
      {/* 自身のデータを含める */}
      <FormControlLabel control={<Switch checked={val.isSelf} name="isSelf" onChange={handleBool} color="primary" />} label="自身のデータを含める" style={{ color: "#888" }} />

      {/* Members */}
      <TextField
        label="members"
        name="members"
        value={val["members"]}
        onChange={handleChange}
        multiline
        minRows={4}
        variant="outlined"
        helperText={"データを取得したい社員番号をカンマ区切りで入力してください。"}
        style={{ marginTop: 10 }}
      />

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