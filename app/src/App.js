import { Container, Paper, Grid, Typography } from "@mui/material";
import Header from "./components/Header";

var codes = ["STB", "VIC", "SSI", "MSN", "FPT", "HAG"]

function App() {
  return (
    <div className="App">
      <Container>
        <Grid container>
          {codes.map(code => (
            <Grid item xs={6}>
              <a href={"/" + code}>
                <Paper sx={{height: "60px", margin: "20px", padding: "20px", display: "flex", justifyContent: "center", alignItems: "center"}}>
                  <Typography sx={{fontWeight: "bold"}}variant="h6">
                    {code}
                  </Typography>
                </Paper>
              </a>
            </Grid>
          ))}
        </Grid>
       </Container>
    </div>
  );
}

export default App;
