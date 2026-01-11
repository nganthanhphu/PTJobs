const Login = ({ route }) => {
    const info = [
        {
            title: "Tên đăng nhập",
            field: "username",
            icon: "account",
        },
        {
            title: "Mật khẩu",
            field: "password",
            icon: "eye",
            secureTextEntry: true,
        },
    ];

    const [user, setUser] = useState({});
    const [err, setErr] = useState(false);
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();
    const [, dispatch] = useContext(MyUserContext);

    const validate = () => {
        // if (!user.password || user.password !== user.confirm) {
        //     setErr(true)
        //     return false;
        // }
        // //...

        // setErr(false);
        return true;
    };

    const login = async () => {
        if (validate() === true) {
            try {
                setLoading(true);
                console.info(user);
                let res = await Apis.post(endpoints["login"], {
                    ...user,
                    client_id: "4jr0cMT5CiZAW3ZAaW5Sx3Ex9JC1yNjnK34k85ga", // Lưu vào biến môi trường của react
                    client_secret:
                        "2gYKjItC9dWyLTpzodprh8P3Pk8TUgkyOuSB1JmVMH3wW6s3e4HgvIw9QGkY7M2w5xLNY1TxMB3pWxPYv0MkmBOMAlYM9PKrPwYdZ9SBEgEZrbg3gbctt5LF965qMNEh", // Lưu vào biến môi trường của react
                    grant_type: "password",
                });

                AsyncStorage.setItem("token", res.data.access_token);

                setTimeout(async () => {
                    let user = await authApis(res.data.access_token).get(
                        endpoints["current_user"]
                    );

                    dispatch({
                        type: "login",
                        payload: user.data,
                    });

                    const next = route.params?.next;
                    if (next) nav.navigate(next);
                }, 500);
            } catch (ex) {
                console.error(ex);
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <View style={MyStyles.padding}>
            <Text style={MyStyles.title}>ĐĂNG NHẬP NGƯỜI DÙNG</Text>
            <ScrollView>
                <HelperText type="error" visible={err}>
                    Mật khẩu KHÔNG khớp!
                </HelperText>

                {info.map((i) => (
                    <TextInput
                        key={i.field}
                        style={MyStyles.margin}
                        value={user[i.field]}
                        onChangeText={(t) => setUser({ ...user, [i.field]: t })}
                        label={i.title}
                        secureTextEntry={i.secureTextEntry}
                        right={<TextInput.Icon icon={i.icon} />}
                    />
                ))}

                <Button
                    loading={loading}
                    disabled={loading}
                    style={MyStyles.margin}
                    icon="login"
                    mode="contained"
                    onPress={login}
                >
                    Đăng nhập
                </Button>
            </ScrollView>
        </View>
    );
};

export default Login;
